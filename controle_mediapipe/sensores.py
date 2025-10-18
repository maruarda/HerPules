# sensors/foot_buttons.py
import threading
import time
from dataclasses import dataclass
from typing import Tuple, Optional

import cv2
import mediapipe as mp


@dataclass
class ROI:
    x: int
    y: int
    w: int
    h: int

    def contains(self, px: float, py: float) -> bool:
        return (self.x <= px <= self.x + self.w) and (self.y <= py <= self.y + self.h)


class FootButtonController:
    """
    Controlador de botões físicos usando MediaPipe Pose.
    Detecta a posição dos pés e aciona:
      - jump_edge: True no frame em que um pé entra na ROI de pulo
      - crouching_hold: True enquanto algum pé está na ROI de agachar
      - start_hold: True enquanto AMBOS os pés estão na ROI de iniciar
    """
    def __init__(
        self,
        cam_index: int = 0,
        jump_roi: ROI = ROI(100, 260, 150, 150),
        crouch_roi: ROI = ROI(380, 260, 150, 150),
        start_roi: ROI = ROI(240, 260, 180, 150),
        show_debug: bool = True,
        min_detection_confidence: float = 0.5,
        min_tracking_confidence: float = 0.5,
        max_fps: int = 30,
    ):
        self.cam_index = cam_index
        self.jump_roi = jump_roi
        self.crouch_roi = crouch_roi
        self.start_roi = start_roi
        self.show_debug = show_debug
        self.min_det = min_detection_confidence
        self.min_track = min_tracking_confidence
        self.max_delay = 1.0 / max_fps

        # estados públicos
        self._jump_edge = False
        self._crouching_hold = False
        self._start_hold = False

        # estados internos
        self._in_jump_area_prev = False
        self._stop = False
        self._thread: Optional[threading.Thread] = None

        # suavização
        self._smooth_alpha = 0.5
        self._left_px = None
        self._left_py = None
        self._right_px = None
        self._right_py = None

    # -----------------------------------------------------------
    # controle de execução
    # -----------------------------------------------------------
    def start(self):
        if self._thread and self._thread.is_alive():
            return
        self._stop = False
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()

    def stop(self):
        self._stop = True
        if self._thread:
            self._thread.join(timeout=1)

    # -----------------------------------------------------------
    # sinais para o jogo
    # -----------------------------------------------------------
    def pop_jump(self) -> bool:
        """Retorna True uma vez na borda de entrada na ROI de pulo."""
        val = self._jump_edge
        self._jump_edge = False
        return val

    @property
    def crouching(self) -> bool:
        """True enquanto houver pé na ROI de agachar."""
        return self._crouching_hold

    @property
    def start_hold(self) -> bool:
        """True enquanto AMBOS os pés estão na ROI de iniciar."""
        return self._start_hold

    # -----------------------------------------------------------
    # loop principal de captura
    # -----------------------------------------------------------
    def _run(self):
        cap = cv2.VideoCapture(self.cam_index, cv2.CAP_DSHOW)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

        mp_pose = mp.solutions.pose
        with mp_pose.Pose(
            model_complexity=1,
            enable_segmentation=False,
            smooth_landmarks=True,
            min_detection_confidence=self.min_det,
            min_tracking_confidence=self.min_track,
        ) as pose:
            while not self._stop:
                t0 = time.time()
                ok, frame = cap.read()
                if not ok:
                    time.sleep(0.05)
                    continue

                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                res = pose.process(frame_rgb)
                h, w = frame.shape[:2]
                left_px, left_py, right_px, right_py = self._extract_feet_pixels(res, w, h)

                # suavização (exponencial)
                if left_px is not None:
                    self._left_px = left_px if self._left_px is None else self._ema(self._left_px, left_px)
                    self._left_py = left_py if self._left_py is None else self._ema(self._left_py, left_py)
                if right_px is not None:
                    self._right_px = right_px if self._right_px is None else self._ema(self._right_px, right_px)
                    self._right_py = right_py if self._right_py is None else self._ema(self._right_py, right_py)

                # -----------------------------------------------------------
                # lógica das ROIs
                # -----------------------------------------------------------
                any_in_jump = (
                    self._foot_in_roi(self._left_px, self._left_py, self.jump_roi)
                    or self._foot_in_roi(self._right_px, self._right_py, self.jump_roi)
                )
                any_in_crouch = (
                    self._foot_in_roi(self._left_px, self._left_py, self.crouch_roi)
                    or self._foot_in_roi(self._right_px, self._right_py, self.crouch_roi)
                )
                both_in_start = (
                    self._foot_in_roi(self._left_px, self._left_py, self.start_roi)
                    and self._foot_in_roi(self._right_px, self._right_py, self.start_roi)
                )

                # borda e níveis
                self._jump_edge = (not self._in_jump_area_prev) and any_in_jump
                self._in_jump_area_prev = any_in_jump
                self._crouching_hold = any_in_crouch
                self._start_hold = both_in_start

                # -----------------------------------------------------------
                # debug visual
                # -----------------------------------------------------------
                if self.show_debug:
                    dbg = frame.copy()

                    # JUMP
                    cv2.rectangle(
                        dbg,
                        (self.jump_roi.x, self.jump_roi.y),
                        (self.jump_roi.x + self.jump_roi.w, self.jump_roi.y + self.jump_roi.h),
                        (0, 200, 255),
                        2,
                    )
                    cv2.putText(
                        dbg,
                        "JUMP",
                        (self.jump_roi.x + 5, self.jump_roi.y - 8),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.6,
                        (0, 200, 255),
                        2,
                    )

                    # CROUCH
                    cv2.rectangle(
                        dbg,
                        (self.crouch_roi.x, self.crouch_roi.y),
                        (self.crouch_roi.x + self.crouch_roi.w, self.crouch_roi.y + self.crouch_roi.h),
                        (255, 150, 0),
                        2,
                    )
                    cv2.putText(
                        dbg,
                        "CROUCH",
                        (self.crouch_roi.x + 5, self.crouch_roi.y - 8),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.6,
                        (255, 150, 0),
                        2,
                    )

                    # START
                    cv2.rectangle(
                        dbg,
                        (self.start_roi.x, self.start_roi.y),
                        (self.start_roi.x + self.start_roi.w, self.start_roi.y + self.start_roi.h),
                        (0, 255, 0),
                        2,
                    )
                    cv2.putText(
                        dbg,
                        "START",
                        (self.start_roi.x + 5, self.start_roi.y - 8),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.6,
                        (0, 255, 0),
                        2,
                    )

                    # pés
                    self._draw_foot_point(dbg, self._left_px, self._left_py, "L")
                    self._draw_foot_point(dbg, self._right_px, self._right_py, "R")

                    # estados
                    cv2.putText(
                        dbg,
                        f"jump_edge: {self._jump_edge}",
                        (10, 20),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.6,
                        (0, 255, 0),
                        2,
                    )
                    cv2.putText(
                        dbg,
                        f"crouching: {self._crouching_hold}",
                        (10, 45),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.6,
                        (0, 255, 0),
                        2,
                    )
                    cv2.putText(
                        dbg,
                        f"start_hold: {self._start_hold}",
                        (10, 70),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.6,
                        (0, 255, 0),
                        2,
                    )

                    cv2.imshow("Foot Buttons (MediaPipe/OpenCV)", dbg)
                    if cv2.waitKey(1) & 0xFF == 27:  # ESC fecha debug
                        self.show_debug = False
                        cv2.destroyWindow("Foot Buttons (MediaPipe/OpenCV)")

                # controle de FPS
                dt = time.time() - t0
                if dt < self.max_delay:
                    time.sleep(self.max_delay - dt)

        cap.release()
        try:
            cv2.destroyAllWindows()
        except:
            pass

    # -----------------------------------------------------------
    # utilitários
    # -----------------------------------------------------------
    def _extract_feet_pixels(self, res, w: int, h: int) -> Tuple[Optional[int], Optional[int], Optional[int], Optional[int]]:
        if not res or not res.pose_landmarks:
            return None, None, None, None
        lm = res.pose_landmarks.landmark
        # LEFT_HEEL=29, RIGHT_HEEL=30, LEFT_FOOT_INDEX=31, RIGHT_FOOT_INDEX=32
        def to_px(idx_a, idx_b):
            ax, ay = lm[idx_a].x * w, lm[idx_a].y * h
            bx, by = lm[idx_b].x * w, lm[idx_b].y * h
            return int((ax + bx) / 2), int((ay + by) / 2)
        lx, ly = to_px(29, 31)
        rx, ry = to_px(30, 32)
        return lx, ly, rx, ry

    def _foot_in_roi(self, px: Optional[float], py: Optional[float], roi: ROI) -> bool:
        if px is None or py is None:
            return False
        return roi.contains(px, py)

    def _ema(self, old: float, new: float) -> float:
        a = self._smooth_alpha
        return a * new + (1 - a) * old

    def _draw_foot_point(self, img, px, py, label):
        if px is None or py is None:
            return
        cv2.circle(img, (int(px), int(py)), 6, (0, 255, 0), -1)
        cv2.putText(img, label, (int(px) + 8, int(py) - 8), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
