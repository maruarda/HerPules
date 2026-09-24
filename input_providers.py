import pygame
import mediapipe as mp
from input_state import InputState
from pose_detector import PoseDetector



class KeyboardInputProvider:
    """Fornece entradas de teclado como comando para o jogo."""

    def get_input(self):
        """Retorna o estado de entrada baseado no teclado.

        Returns:
            InputState: Estado atual da entrada com flags de pulo e agachar.
        """
        estado = InputState()
        keys = pygame.key.get_pressed()
        estado.abaixar = keys[pygame.K_DOWN]
        return estado

    def calibrar(self):
        """Método de compatibilidade sem comportamento específico para teclado."""
        pass


class ScriptedInputProvider:
    """Gera uma sequência pré-definida de entradas para testes automatizados."""

    def __init__(self):
        """Inicializa o contador de frames da sequência scriptada."""
        self.frame = 0

    def get_input(self):
        """Retorna um estado de entrada com base em um frame programado.

        Returns:
            InputState: Estado do frame atual da sequência.
        """
        estado = InputState()

        if self.frame == 60:
            estado.pular = True

        if 180 <= self.frame <= 240:
            estado.abaixar = True

        self.frame += 1
        return estado

    def calibrar(self):
        """Método de compatibilidade sem comportamento específico para o modo scriptado."""
        pass


class MediapipeInputProvider:
    """Converte a pose detectada em comandos de pulo e agachar do jogo.

    Esse provedor usa a detecção de landmarks do corpo para interpretar o
    movimento do jogador e gerar ações de entrada em tempo real.
    """

    def __init__(self):
        """Inicializa o detector de pose e os parâmetros de calibração e detecção."""
        self.detector = PoseDetector()
        self.baseline_hip_y = None
        self.baseline_foot_y = None
        self.cooldown_pulo = 0
        self.pose_landmark = mp.solutions.pose.PoseLandmark
        self.hip_y_anterior = None
        self.frames_sem_pose = 0
        self.limiar_pulo = 0.03
        self.limiar_subida = 0.008
        self.limiar_agachar = 0.05

    def release(self):
        """Libera os recursos do detector de pose."""
        self.detector.release()

    def calibrar(self):
        """Calcula as linhas base de quadril e tornozelo para interpretar movimento humano.

        Coleta vários frames da câmera e calcula a média da posição do quadril e
        dos tornozelos para servir de referência durante o jogo.
        """
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
        """Interpreta a pose atual e retorna um estado de entrada do jogador.

        Returns:
            InputState: Estado com pulo e/ou agachar conforme a pose detectada.
        """
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

        feet_up = foot_y < self.baseline_foot_y - 0.02
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
