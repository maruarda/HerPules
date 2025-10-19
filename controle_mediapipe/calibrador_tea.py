#################################################################################
######################### SOFTWARE BASE - PROJETO T-TEA #########################
#################################################################################
################################# VERSÃO 1.0 ####################################
#################################################################################
import csv
import cv2
import mediapipe as mp
import numpy as np
import pygame
import time
import random
import controle_mediapipe.settings

pygame.init()
#################################################################################
################################## Hora de Inicio ###############################
#################################################################################
inicio_da_sessao=False
if inicio_da_sessao==False:
    inicio_da_sessao_t0 = int(time.time())
    inicio_da_sessao=True
#################################################################################
#################################### Hardware ###################################
#################################################################################
# Tamanho das Telas:
largura_projetor = 800  # A ltere este valor de acordo com a resolução da projeção do jogo.
altura_projetor = 600  # A ltere este valor de acordo com a resolução da projeção do jogo.
largura_tela_controle = 640  # Esta tela é usada pelo terapeuta/operador. Altere o valor caso necessário.
altura_tela_controle = 480  # Esta tela é usada pelo terapeuta/operador. Altere o valor caso necessário.
relacao_largura = (largura_projetor / largura_tela_controle)  # Esta relação é usada na correção de perspectiva.
relacao_altura = (altura_projetor / altura_tela_controle)  # Esta relação é usada na correção de perspectiva.
tela_de_calibracao = np.zeros((altura_projetor, largura_projetor, 3),
                            np.uint8)  # Tela que será usada para o projetar o jogo.
tela_de_controle = np.zeros((altura_tela_controle, largura_tela_controle, 3),
                            np.uint8)  # Tela que será usada para o projetar o jogo.


csv.register_dialect(
    'mydialect',
    delimiter = ';',
    quotechar = '"',
    doublequote = True,
    skipinitialspace = True,
    lineterminator = '\n',
    quoting = csv.QUOTE_MINIMAL)


#################################################################################
################################## SPRITES ######################################
#################################################################################
icone_fig=pygame.image.load('Assets/Repetea_Figuras/icone.png')
atencao_perto_fig=pygame.image.load('Assets/Repetea_Figuras/atencao_perto.png')
atencao_longe_fig=pygame.image.load('Assets/Repetea_Figuras/atencao_longe.png')
trofeu_fig=pygame.image.load('Assets/Repetea_Figuras/trofeu.png')
trofeu_25_fig=pygame.image.load('Assets/Repetea_Figuras/trofeu_25.png')
trofeu_50_fig=pygame.image.load('Assets/Repetea_Figuras/trofeu_50.png')
trofeu_75_fig=pygame.image.load('Assets/Repetea_Figuras/trofeu_75.png')
triste_fig=pygame.image.load('Assets/Repetea_Figuras/triste.png')
feliz_fig=pygame.image.load('Assets/Repetea_Figuras/feliz.png')
vez_do_jogador_verde_1_fig=pygame.image.load('Assets/Repetea_Figuras/vez_do_jogador_verde_1.png')
vez_do_jogador_verde_2_fig=pygame.image.load('Assets/Repetea_Figuras/vez_do_jogador_verde_2.png')
base_com_pe_fig=pygame.image.load('Assets/Repetea_Figuras/base_com_pe.png')
base_com_pe_verde_fig=pygame.image.load('Assets/Repetea_Figuras/base_com_pe_verde.png')
base_com_pe_vermelho_fig=pygame.image.load('Assets/Repetea_Figuras/base_com_pe_vermelho.png')
base_sem_pe_fig=pygame.image.load('Assets/Repetea_Figuras/base_sem_pe.png')
avisos_fig=pygame.image.load('Assets/Repetea_Figuras/avisos.png')
ajuda_f1_fig=pygame.image.load('Assets/Repetea_Figuras/ajuda_F1.png')
instrucao_calibrar_fig=pygame.image.load('Assets/Repetea_Figuras/calibrar.png')
calibracao_finalizada_fig=pygame.image.load('Assets/Repetea_Figuras/calibracao_ok.png')
repetea_inciar_fig=pygame.image.load('Assets/Repetea_Figuras/base_com_iniciar.png')
pausa_fig=pygame.image.load('Assets/Repetea_Figuras/pause.png')
sem_sinal_fig=pygame.image.load('Assets/Repetea_Figuras/sem_sinal.png')
tempo_fig=pygame.image.load('Assets/Repetea_Figuras/tempo.png')
som_fig=pygame.image.load('Assets/Repetea_Figuras/som.png')
hud_on_fig=pygame.image.load('Assets/Repetea_Figuras/hud_on.png')
hud_off_fig=pygame.image.load('Assets/Repetea_Figuras/hud_off.png')
posicionamento_fig=pygame.image.load('Assets/Repetea_Figuras/posicionamento.png')
fase_abaixo_fig=pygame.image.load('Assets/Repetea_Figuras/fase_abaixo.png')
fase_acima_fig=pygame.image.load('Assets/Repetea_Figuras/fase_acima.png')
silhueta_perto_fig=pygame.image.load('Assets/Repetea_Figuras/silhueta_perto.png')
silhueta_longe_fig=pygame.image.load('Assets/Repetea_Figuras/silhueta_longe.png')
triagulo_longe_selecionado_fig=pygame.image.load('Assets/Repetea_Figuras/triangulo_selecionado_longe.png')
triagulo_longe_selecionado_ajuda_fig=pygame.image.load('Assets/Repetea_Figuras/triangulo_selecionado_longe_ajuda.png')
retangulo_longe_selecionado_fig=pygame.image.load('Assets/Repetea_Figuras/retangulo_selecionado_longe.png')
retangulo_longe_selecionado_ajuda_fig=pygame.image.load('Assets/Repetea_Figuras/retangulo_selecionado_longe_ajuda.png')
circulo_longe_selecionado_fig=pygame.image.load('Assets/Repetea_Figuras/circulo_selecionado_longe.png')
circulo_longe_selecionado_ajuda_fig=pygame.image.load('Assets/Repetea_Figuras/circulo_selecionado_longe_ajuda.png')
quadrado_longe_selecionado_fig=pygame.image.load('Assets/Repetea_Figuras/quadrado_selecionado_longe.png')
quadrado_longe_selecionado_ajuda_fig=pygame.image.load('Assets/Repetea_Figuras/quadrado_selecionado_longe_ajuda.png')
triagulo_perto_selecionado_fig=pygame.image.load('Assets/Repetea_Figuras/triangulo_selecionado_perto.png')
triagulo_perto_selecionado_ajuda_fig=pygame.image.load('Assets/Repetea_Figuras/triangulo_selecionado_perto_ajuda.png')
retangulo_perto_selecionado_fig=pygame.image.load('Assets/Repetea_Figuras/retangulo_selecionado_perto.png')
retangulo_perto_selecionado_ajuda_fig=pygame.image.load('Assets/Repetea_Figuras/retangulo_selecionado_perto_ajuda.png')
circulo_perto_selecionado_fig=pygame.image.load('Assets/Repetea_Figuras/circulo_selecionado_perto.png')
circulo_perto_selecionado_ajuda_fig=pygame.image.load('Assets/Repetea_Figuras/circulo_selecionado_perto_ajuda.png')
quadrado_perto_selecionado_fig=pygame.image.load('Assets/Repetea_Figuras/quadrado_selecionado_perto.png')
quadrado_perto_selecionado_ajuda_fig=pygame.image.load('Assets/Repetea_Figuras/quadrado_selecionado_perto_ajuda.png')


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
############################# VARIÁVEIS DE PROGRAMA #############################
#################################################################################
mp_drawing = mp.solutions.drawing_utils  # Configuração do MediaPipe. Ver https://google.github.io/mediapipe/solutions/pose.html para maiores detalhes.
mp_pose = mp.solutions.pose  # Configuração do MediaPipe. Ver https://google.github.io/mediapipe/solutions/pose.html para maiores detalhes.
pontos_calibracao = np.zeros((4, 2), int)  # Matriz para os pontos de calibração de perspectiva - 4 linhas/ 2 colunas
contador = 0  # Contador utilizado nos 4 pontos de calibração
figura_selecionada=False # Usada para evitar que o usuário apenas selecione uma vez a figura e não ficar piscando
lista_sorteio=[] #São as figuras sorteadas pelo computador e colocadas nesta lista, para depois fazer a comparação com as escolhas do usuário
pontuacao=0 # Pontos conseguidos em durante a rodada
tempo_ajuda=5 # Tempo até a ajuda aparecer
tempo_total=10 # Tempo máximo da jogada
atencao_memorizar=False
hud_switch=True
pausa_switch=False
tempo_ajuda_switch=False
tentativa=1
x_pose = 0
y_pose = 0

def resetar_vars():

    global pontos_calibracao, contador

    #pygame.init()

    #relacao_largura = (largura_projetor / largura_tela_controle)  # Esta relação é usada na correção de perspectiva.
    #relacao_altura = (altura_projetor / altura_tela_controle)  # Esta relação é usada na correção de perspectiva.
    #tela_de_calibracao = np.zeros((altura_projetor, largura_projetor, 3), np.uint8)  # Tela que será usada para o projetar o jogo.
    #tela_de_controle = np.zeros((altura_tela_controle, largura_tela_controle, 3), np.uint8)  # Tela que será usada para o projetar o jogo.

    #mp_drawing = mp.solutions.drawing_utils  # Configuração do MediaPipe. Ver https://google.github.io/mediapipe/solutions/pose.html para maiores detalhes.
    #mp_pose = mp.solutions.pose  # Configuração do MediaPipe. Ver https://google.github.io/mediapipe/solutions/pose.html para maiores detalhes.
    pontos_calibracao = np.zeros((4, 2), int)  # Matriz para os pontos de calibração de perspectiva - 4 linhas/ 2 colunas
    contador = 0  # Contador utilizado nos 4 pontos de calibração
    #hud_switch=True
    #pausa_switch=False
    #tempo_ajuda_switch=False
    #tentativa=1
    #x_pose = 0
    #y_pose = 0


def calibrar_ttea():

    global gameDisplay#, x_pose, y_pose

    resetar_vars()

    camera = cv2.VideoCapture(0)

    gameWarning = pygame.display.set_mode((largura_projetor, altura_projetor))
    pygame.display.set_caption('T-TEA')
    pygame.display.set_icon(icone_fig)
    gameWarning.blit(avisos_fig,(0, 0))
    pygame.display.update()
    gameWarning=False
    gameExit=False # Sai do completamente do jogo

    while not gameWarning:
        for event in pygame.event.get():
            # SAIR ou CONCORDO
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    gameDisplay = pygame.display.set_mode((largura_projetor, altura_projetor))
                    pygame.display.set_caption('T-TEA')
                    pygame.display.set_icon(icone_fig)
                    instrucao_calibrar()
                    pygame.display.update()
                    gameWarning=True
                if event.key == pygame.K_q:
                    gameExit = True
                    cv2.destroyWindow('tela_de_controle')
                    pygame.quit()
                    camera.release()
                    gameWarning = True
                    exit()


    #################################################################################
    #################### Inicialização do MediaPipe e Calibração ####################
    #################################################################################
    while not gameExit:

        with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
            if camera.isOpened():
                ret, frame = camera.read()

                # Tela de Controle para RGB.
                tela_de_controle = cv2.cvtColor(cv2.flip(frame,1), cv2.COLOR_BGR2RGB)
                tela_de_controle.flags.writeable = False

                # Detecção.
                results = pose.process(tela_de_controle)

                # Tela de Controle para BGR.
                tela_de_controle.flags.writeable = True
                tela_de_controle = cv2.cvtColor(tela_de_controle, cv2.COLOR_RGB2BGR)

                # Antes da Calibração.
                #if contador <= 3:
                cv2.circle(tela_de_controle, (pontos_calibracao[0]), 5, azul, 3)
                cv2.circle(tela_de_controle, (pontos_calibracao[1]), 5, azul, 3)
                cv2.circle(tela_de_controle, (pontos_calibracao[2]), 5, azul, 3)
                cv2.circle(tela_de_controle, (pontos_calibracao[3]), 5, azul, 3)
                pygame.display.update()
                # Depois da Calibração.
                if contador == 4:
                    cv2.line(tela_de_controle, (pontos_calibracao[0]), (pontos_calibracao[1]), (verde), 2)
                    cv2.line(tela_de_controle, (pontos_calibracao[1]), (pontos_calibracao[3]), (verde), 2)
                    cv2.line(tela_de_controle, (pontos_calibracao[2]), (pontos_calibracao[0]), (verde), 2)
                    cv2.line(tela_de_controle, (pontos_calibracao[2]), (pontos_calibracao[3]), (verde), 2)

                #    cv2.circle(tela_de_controle, (pontos_calibracao[0]), 5, azul, 3)
                 #   cv2.circle(tela_de_controle, (pontos_calibracao[1]), 5, azul, 3)
                  #  cv2.circle(tela_de_controle, (pontos_calibracao[2]), 5, azul, 3)
                   # cv2.circle(tela_de_controle, (pontos_calibracao[3]), 5, azul, 3)
                    gameDisplay = pygame.display.set_mode((largura_projetor, altura_projetor))
                    pygame.display.set_caption('Calibracao')
                    pygame.display.set_icon(icone_fig)

                    calibracao_ok()
                    tela_update()
                    pass
                # Extração de coordenadas de pontos de referência.
                try:
                    landmarks = results.pose_landmarks.landmark
                    #x_pose = landmarks[mp_pose.PoseLandmark.NOSE.value].x  # 33 Pontos de referência do MediaPipe. Ex: RIGHT_FOOT_INDEX; NOSE; RIGHT_INDEX
                    #y_pose = landmarks[mp_pose.PoseLandmark.NOSE.value].y  # 33 Pontos de referência do MediaPipe. Ex: RIGHT_FOOT_INDEX; NOSE; RIGHT_INDEX
                    x_pose = (landmarks[mp_pose.PoseLandmark.RIGHT_FOOT_INDEX.value].x + landmarks[
                        mp_pose.PoseLandmark.LEFT_FOOT_INDEX.value].x) / 2
                    y_pose = (landmarks[mp_pose.PoseLandmark.RIGHT_FOOT_INDEX.value].y + landmarks[
                        mp_pose.PoseLandmark.LEFT_FOOT_INDEX.value].y) / 2

                    # Desenho dos pontos de referência
                    mp_drawing.draw_landmarks(tela_de_controle, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                            mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2),
                                            mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=2, circle_radius=2)
                                            )

                except:
                    pass

                # Atualização das telas
                cv2.imshow("TELA DE CONTROLE", tela_de_controle)
                cv2.setMouseCallback("TELA DE CONTROLE", mousePoints)

                # Teclas de Atalho
                for event in pygame.event.get():
                    # SAIR
                    if event.type == pygame.QUIT:
                        gameExit=True
                        cv2.destroyWindow("TELA DE CONTROLE")
                        grava_calibracao()
                        print('P1: ', pontos_calibracao[0], ' P2: ', pontos_calibracao[1], ' P3: ', pontos_calibracao[2], ' P4: ', pontos_calibracao[3])
                        pygame.display.quit()
                        camera.release()

                # SAIR (ESC)
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_q:
                            gameExit = True
                            cv2.destroyWindow("TELA DE CONTROLE")
                            grava_calibracao()
                            print('P1: ', pontos_calibracao[0], ' P2: ', pontos_calibracao[1], ' P3: ', pontos_calibracao[2], ' P4: ', pontos_calibracao[3])
                            pygame.display.quit()
                            camera.release()

                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            gameExit = True
                            cv2.destroyWindow("TELA DE CONTROLE")
                            grava_calibracao()
                            print('P1: ', pontos_calibracao[0], ' P2: ', pontos_calibracao[1], ' P3: ', pontos_calibracao[2], ' P4: ', pontos_calibracao[3])
                            pygame.display.quit()
                            camera.release()

#################################################################################
################################### FUNÇÕES #####################################
#################################################################################
def avisos(): #Tela inicial com os avisos do equipamento
    global gameDisplay
    gameDisplay.blit(avisos_fig,(0, 0))

def instrucao_calibrar():
    global gameDisplay
    gameDisplay.blit(instrucao_calibrar_fig, (0, 0))

def ajuda_f1(): #Tela com as teclas de atalho
    global gameDisplay
    gameDisplay.blit(ajuda_f1_fig, (0, 0))

def posicionamento():
    global gameDisplay
    gameDisplay.blit(posicionamento_fig, (0, 0))

def sem_sinal():
    global gameDisplay
    gameDisplay.blit(sem_sinal_fig, (0, 0))

def calibracao_ok():
    global gameDisplay
    gameDisplay.blit(calibracao_finalizada_fig, (0, 0))

def fill_preto():
    global gameDisplay
    gameDisplay.fill(preto)

def mousePoints(event, x, y, flags, params):
    # Função para capturar cliques do Mouse:
    global contador
    if event == cv2.EVENT_LBUTTONDOWN:
        pontos_calibracao[contador] = x, y
        contador = contador + 1

def posicao():

    # Função para determinar a posição do jogador na área de projeçao:
    # Transformação de Perspectiva:
    pts1 = np.float32([pontos_calibracao[0], pontos_calibracao[1], pontos_calibracao[2], pontos_calibracao[3]])
    pts2 = np.float32(
        [[0, 0], [largura_tela_controle, 0], [0, altura_tela_controle], [largura_tela_controle, altura_tela_controle]])
    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    perspectiva = cv2.warpPerspective(tela_de_controle, matrix, (largura_tela_controle, altura_tela_controle))

    # Posição do jogador:
    p = (int(x_pose * largura_tela_controle), int(y_pose * altura_tela_controle))
    position_x = (matrix[0][0] * p[0] + matrix[0][1] * p[1] + matrix[0][2]) / (
    (matrix[2][0] * p[0] + matrix[2][1] * p[1] + matrix[2][2]))
    position_y = (matrix[1][0] * p[0] + matrix[1][1] * p[1] + matrix[1][2]) / (
    (matrix[2][0] * p[0] + matrix[2][1] * p[1] + matrix[2][2]))
    p_after = (int((position_x) * (relacao_largura)), int((position_y) * (relacao_altura)))

    return p_after

def rand():
    #Função para sortear a figura
    rand_figura = round(random.randrange(0, 4))
    return rand_figura

def delay():
    time.sleep(0.5)

def tela_update():
    pygame.display.update()

def grava_calibracao():
    Config = ['Ponto 1 x', 'Ponto 1 y', 'Ponto 2 x', 'Ponto 2 y', 'Ponto 3 x', 'Ponto 3 y', 'Ponto 4 x', 'Ponto 4 y']
    Dados =  [pontos_calibracao[0][0], pontos_calibracao[0][1], pontos_calibracao[1][0], pontos_calibracao[1][1], pontos_calibracao[2][0], pontos_calibracao[2][1], pontos_calibracao[3][0], pontos_calibracao[3][1]]
    file = 'calibracao.csv'

    with open(file, 'w') as csvfile:
        csvwriter = csv.writer(csvfile, dialect='mydialect')
        csvwriter.writerow(Config)
        csvwriter.writerow(Dados)
