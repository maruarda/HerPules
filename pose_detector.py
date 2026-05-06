import cv2
import mediapipe as mp

class PoseDetector:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            print("Erro: não foi possível abrir a câmera.")
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose()

    def read_pose(self):
        ok, frame = self.cap.read()
        if not ok:
            print("Erro: não foi possível ler frame da câmera.")
            return None

        # mostra a câmera SEMPRE, mesmo sem landmarks
        cv2.imshow("Camera", frame)
        cv2.waitKey(1)

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        resultado = self.pose.process(rgb)
        # print(resultado.pose_landmarks)  # Debug: Imprime os landmarks detectados

        if not resultado.pose_landmarks:
            return None

        return resultado.pose_landmarks.landmark

    def release(self):
        if self.cap is not None:
            self.cap.release()
        cv2.destroyAllWindows()
     