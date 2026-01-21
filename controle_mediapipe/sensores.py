import cv2
import mediapipe as mp
import numpy as np

from controle_mediapipe.settings import *

mp_drawing = mp.solutions.drawing_utils
mp_poses = mp.solutions.pose


def posicao(x, y):
    p_webcam = (int(x * largura_webcam), int(y * altura_webcam))

    pts1 = np.float32(pontos_calibracao)
    pts2 = np.float32([
        [0, 0],
        [largura_projetor, 0],
        [0, altura_projetor],
        [largura_projetor, altura_projetor]
    ])

    matrix = cv2.getPerspectiveTransform(pts1, pts2)

    position_x = (matrix[0][0] * p_webcam[0] + matrix[0][1] * p_webcam[1] + matrix[0][2]) / (
        (matrix[2][0] * p_webcam[0] + matrix[2][1] * p_webcam[1] + matrix[2][2]))
    position_y = (matrix[1][0] * p_webcam[0] + matrix[1][1] * p_webcam[1] + matrix[1][2]) / (
        (matrix[2][0] * p_webcam[0] + matrix[2][1] * p_webcam[1] + matrix[2][2]))

    return int(position_x), int(position_y)


def area_calibracao(x, y):
    p_webcam = (int(x * largura_webcam), int(y * altura_webcam))
    polygon = np.array([
        pontos_calibracao[0],
        pontos_calibracao[1],
        pontos_calibracao[3],
        pontos_calibracao[2]
    ], np.int32)

    return cv2.pointPolygonTest(polygon, p_webcam, False) >= 0


class Sensores:
    def __init__(self):
        self.pose_tracking = mp_poses.Pose(
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        self.feet_x = 0
        self.feet_y = 0
        self.pose_detected = False
        self.feet_in_calibration_area = False

    def scan_feets(self, image):
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        results = self.pose_tracking.process(image)
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        if results.pose_landmarks:
            self.pose_detected = True

            foot1 = results.pose_landmarks.landmark[31]
            foot2 = results.pose_landmarks.landmark[32]

            x = (foot1.x + foot2.x) / 2
            y = (foot1.y + foot2.y) / 2

            self.feet_in_calibration_area = area_calibracao(x, y)
            self.feet_x, self.feet_y = posicao(x, y)

        else:
            self.pose_detected = False
            self.feet_in_calibration_area = False

        return image

    def get_feet_center(self):
        return self.feet_x, self.feet_y
