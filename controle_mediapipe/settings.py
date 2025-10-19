import os
import pygame
import numpy as np
import cv2


pwd = os.path.dirname(__file__)
path_assets = os.path.join(pwd, "assets")

tamanho_tela = 800, 600
fps = 60

# Variáveis do Pygame
WINDOW_NAME = "HerPules"
GAME_TITLE = WINDOW_NAME
CAMERA = 0
CAMERA_FLIP = 0
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600


CONTADOR = 0

# Load calibration points from CSV if it exists
csv_path = os.path.join(pwd, "../calibracao.csv")
if os.path.exists(csv_path):
    try:
        import csv

        with open(csv_path, "r") as f:
            reader = csv.reader(f, delimiter=";")
            next(reader)  # Skip header
            data = next(reader)  # Read data row
            # Convert the flat list to (4, 2) array
            pontos_calibracao = np.array(
                [
                    [int(data[0]), int(data[1])],  # Point 1
                    [int(data[2]), int(data[3])],  # Point 2
                    [int(data[4]), int(data[5])],  # Point 3
                    [int(data[6]), int(data[7])],  # Point 4
                ],
                dtype=int,
            )
    except Exception as e:
        print(f"Error loading calibration data: {e}")
        pontos_calibracao = np.zeros((4, 2), int)
else:
    pontos_calibracao = np.zeros((4, 2), int)
div0_pista = 0
div1_pista = SCREEN_WIDTH // 3
div2_pista = 2 * (SCREEN_WIDTH // 3)
div3_pista = SCREEN_WIDTH

pista = 1
score = 0
movimento = 0
Alvo = 0
Alvo_c = 0
Alvo_d = 0
Obst = 0
Obst_c = 0
Obst_d = 0


FPS = 60
DRAW_FPS = False

# sizes
BUTTONS_SIZES = (150, 45)
CAR_SIZE = int(SCREEN_WIDTH / 5)
CAR_HITBOX_SIZE = (CAR_SIZE + 50, CAR_SIZE + 50)
TARGETS_SIZES = (100, 100)
OBSTACLE_SIZES = (100, 100)

OBJ_POS = [(368, 80), (393, 80), (419, 80)]
"""
OBJ_POS_F = [(104, 600), (337, 600),(570, 600)]

264, 56, 151
0.5, 0.1, 0.3
"""

# drawing
DRAW_HITBOX = False  # will draw all the hitbox

# animation
ANIMATION_SPEED = 0.01  # the frame of the insects will change every X sec

# difficulty
GAME_DURATION = 30  # the game will last X sec
TIME_PAST = 0

TARGETS_SPAWN_TIME = 8
TARGETS_MOVE_SPEED = 1
OBSTACLE_PENALITY = (
    0  # will remove X of the score of the player (if he colides with a obstacle)
)

# colors
COLORS = {
    "title": (38, 61, 39),
    "score": (38, 61, 39),
    "timer": (38, 61, 39),
    "buttons": {
        "default": (56, 67, 209),
        "second": (87, 99, 255),
        "text": (255, 255, 255),
        "shadow": (46, 54, 163),
    },
}  # second is the color when the mouse is on the button

# sounds / music
MUSIC_VOLUME = 0  # value between 0 and 1
SOUNDS_VOLUME = 1

# fonts
pygame.font.init()
FONTS = {}
FONTS["small"] = pygame.font.Font(None, 10)
FONTS["medium"] = pygame.font.Font(None, 25)
FONTS["big"] = pygame.font.Font(None, 50)

#

# coisas do t-tea
MENU = "Inicial"

#################################################################################
################################## CORES & FONTES ###############################
#################################################################################
azul = 0, 0, 255
verde = 0, 255, 0
vermelho = 255, 0, 0
amarelo = 255, 255, 0
branco = 255, 255, 255
preto = 0, 0, 0

fonte = cv2.FONT_HERSHEY_SIMPLEX
font = pygame.font.SysFont(None, 25)


#################################################################################
#################################### Hardware ###################################
#################################################################################
# Tamanho das Telas:
largura_projetor = (
    SCREEN_WIDTH  # A ltere este valor de acordo com a resolução da projeção do jogo.
)
altura_projetor = (
    SCREEN_HEIGHT  # A ltere este valor de acordo com a resolução da projeção do jogo.
)
largura_tela_controle = (
    640  # Esta tela é usada pelo terapeuta/operador. Altere o valor caso necessário.
)
altura_tela_controle = (
    480  # Esta tela é usada pelo terapeuta/operador. Altere o valor caso necessário.
)

# Webcam resolution (will be set by Camera class)
largura_webcam = 640
altura_webcam = 480
relacao_largura = (
    largura_projetor / largura_tela_controle
)  # Esta relação é usada na correção de perspectiva.
relacao_altura = (
    altura_projetor / altura_tela_controle
)  # Esta relação é usada na correção de perspectiva.
tela_de_calibracao = np.zeros(
    (altura_projetor, largura_projetor, 3), np.uint8
)  # Tela que será usada para o projetar o jogo.
tela_de_controle = np.zeros(
    (altura_tela_controle, largura_tela_controle, 3), np.uint8
)  # Tela que será usada para o projetar o jogo.
