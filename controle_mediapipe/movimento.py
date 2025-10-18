import cv2
import mediapipe as mp

class DetectorPulo:
    def __init__(self, jump_threshold=30):
        self.jump_threshold = jump_threshold
        self.baseline_y = None
        self.is_in_air = False

        # Inicializa o MediaPipe Pose
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose()
        self.mp_drawing = mp.solutions.drawing_utils

        # Inicializa câmera
        self.cap = cv2.VideoCapture(0)

    def detectar_pulo(self):
        """Processa um frame da câmera e retorna True apenas no instante em que detecta um pulo."""
        ret, frame = self.cap.read()
        if not ret:
            return False

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.pose.process(rgb)
        pulou = False

        if results.pose_landmarks:
            landmarks = results.pose_landmarks.landmark
            left_ankle = landmarks[self.mp_pose.PoseLandmark.LEFT_ANKLE.value]
            right_ankle = landmarks[self.mp_pose.PoseLandmark.RIGHT_ANKLE.value]
            avg_ankle_y = (left_ankle.y + right_ankle.y) / 2

            h, w, _ = frame.shape
            ankle_pixel_y = int(avg_ankle_y * h)

            if self.baseline_y is None:
                self.baseline_y = ankle_pixel_y

            # Detecta o pulo
            if self.baseline_y - ankle_pixel_y > self.jump_threshold and not self.is_in_air:
                pulou = True
                self.is_in_air = True
                print("Pulou!")

            # Detecta quando volta ao chão
            elif self.is_in_air and ankle_pixel_y >= self.baseline_y - 5:
                self.is_in_air = False

            # Desenho opcional na janela
            self.mp_drawing.draw_landmarks(frame, results.pose_landmarks, self.mp_pose.POSE_CONNECTIONS)
            cv2.line(frame, (0, self.baseline_y), (w, self.baseline_y), (0, 255, 0), 2)
            cv2.circle(frame, (w // 2, ankle_pixel_y), 10, (0, 0, 255), -1)

        cv2.imshow("Detecção de Pulo (Pés)", frame)
        if cv2.waitKey(1) & 0xFF == 27:
            self.cap.release()
            cv2.destroyAllWindows()
            exit()

        return pulou
