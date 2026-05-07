import pygame
import mediapipe as mp
from input_state import InputState
from pose_detector import PoseDetector



class KeyboardInputProvider:
    def get_input(self):
        estado = InputState()
        keys = pygame.key.get_pressed()
        estado.abaixar = keys[pygame.K_DOWN]
        return estado

    def calibrar(self):
        pass


class ScriptedInputProvider:
    def __init__(self):
        self.frame = 0

    def get_input(self):
        estado = InputState()

        if self.frame == 60:
            estado.pular = True

        if 180 <= self.frame <= 240:
            estado.abaixar = True

        self.frame += 1
        return estado

    def calibrar(self):
        pass


class MediapipeInputProvider:
    def __init__(self):
        self.detector = PoseDetector()
        self.baseline_hip_y = None
        self.baseline_foot_y = None
        self.cooldown_pulo = 0
        self.pose_landmark = mp.solutions.pose.PoseLandmark
        self.hip_y_anterior = None
        self.frames_sem_pose = 0
        self.limiar_pulo = 0.06
        self.limiar_subida = 0.015
        self.limiar_agachar = 0.05

    def release(self):
        self.detector.release()

    def calibrar(self):
        valores_hip = []
        valores_foot = []

        for _ in range(30):
            landmarks = self.detector.read_pose()
            if landmarks:
                left_hip = landmarks[self.pose_landmark.LEFT_HIP]
                right_hip = landmarks[self.pose_landmark.RIGHT_HIP]

                hip_y = (left_hip.y + right_hip.y) / 2
                valores_hip.append(hip_y)

                left_ankle = landmarks[self.pose_landmark.LEFT_ANKLE]
                right_ankle = landmarks[self.pose_landmark.RIGHT_ANKLE]

                foot_y = (left_ankle.y + right_ankle.y) / 2
                valores_foot.append(foot_y)

        if valores_hip:
            self.baseline_hip_y = sum(valores_hip) / len(valores_hip)

        if valores_foot:
            self.baseline_foot_y = sum(valores_foot) / len(valores_foot)

    def get_input(self):
        estado = InputState()
        landmarks = self.detector.read_pose()

        if landmarks is None:
            self.frames_sem_pose += 1
            return estado

        self.frames_sem_pose = 0

        left_hip = landmarks[self.pose_landmark.LEFT_HIP]
        right_hip = landmarks[self.pose_landmark.RIGHT_HIP]
        hip_y = (left_hip.y + right_hip.y) / 2

        left_ankle = landmarks[self.pose_landmark.LEFT_ANKLE]
        right_ankle = landmarks[self.pose_landmark.RIGHT_ANKLE]

        foot_y = (left_ankle.y + right_ankle.y) / 2

        if self.baseline_hip_y is None:
            self.baseline_hip_y = hip_y
            self.hip_y_anterior = hip_y
            return estado

        if self.hip_y_anterior is None:
            self.hip_y_anterior = hip_y
            return estado
        
        if self.baseline_foot_y is None:
            self.baseline_foot_y = foot_y
            return estado

        delta_y = self.hip_y_anterior - hip_y
        self.hip_y_anterior = hip_y

        if self.cooldown_pulo > 0:
            self.cooldown_pulo -= 1

        feet_up = foot_y < self.baseline_foot_y - 0.04
        hip_up = hip_y < self.baseline_hip_y - self.limiar_pulo

        if (
            hip_up
            and feet_up
            and delta_y > self.limiar_subida
            and self.cooldown_pulo == 0
        ):
            estado.pular = True
            self.cooldown_pulo = 15

        if hip_y > self.baseline_hip_y + self.limiar_agachar:
            estado.abaixar = True

        return estado
