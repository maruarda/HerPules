import cv2
import mediapipe as mp


class PoseDetector:
    def __init__(self, camera_index=0, mostrar_camera=True, mostrar_landmarks=True):
        # configuração da câmera
        self.cap = cv2.VideoCapture(camera_index)

        if not self.cap.isOpened():
            print("Erro: não foi possível abrir a câmera.")

        # resolução menor = melhor desempenho
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

        # configurações do mediapipe
        self.mp_pose = mp.solutions.pose
        self.mp_drawing = mp.solutions.drawing_utils

        self.pose = self.mp_pose.Pose(
            static_image_mode=False,
            model_complexity=1,
            smooth_landmarks=True,
            enable_segmentation=False,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )

        # flags visuais
        self.mostrar_camera = mostrar_camera
        self.mostrar_landmarks = mostrar_landmarks

        self.frame_skip = 0
        self.last_landmarks = None

    def read_pose(self):
        if self.cap is None or not self.cap.isOpened():
            return None

        ok, frame = self.cap.read()

        if not ok:
            print("Erro: não foi possível ler frame da câmera.")
            return None

        # espelha imagem
        frame = cv2.flip(frame, 1)

        # FRAME SKIP - processa pose só a cada 2 frames para melhorar desempenho

        self.frame_skip += 1

        if self.frame_skip % 2 != 0:
            return self.last_landmarks

        # PROCESSAMENTO MEDIAPIPE

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        rgb.flags.writeable = False

        resultado = self.pose.process(rgb)

        rgb.flags.writeable = True

        # desenha landmarks
        if (
            self.mostrar_landmarks
            and resultado.pose_landmarks
        ):
            self.mp_drawing.draw_landmarks(
                frame,
                resultado.pose_landmarks,
                self.mp_pose.POSE_CONNECTIONS
            )

        # mostra câmera
        if self.mostrar_camera:
            cv2.imshow("Camera", frame)
            cv2.waitKey(1)

        # sem pose detectada
        if not resultado.pose_landmarks:
            return self.last_landmarks

        # salva landmarks
        self.last_landmarks = resultado.pose_landmarks.landmark

        return self.last_landmarks

    def release(self):
        if self.cap is not None:
            self.cap.release()

        self.pose.close()

        cv2.destroyAllWindows()
