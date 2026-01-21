import pygame
import sys
import os
import cv2 as cv
from entidades.hercules import Hercules
from entidades.chao import Chao
from entidades.ceu import Ceu
from entidades.obstaculos import Obstaculo
from entidades.iniciar import Botao
from controle_mediapipe.calibrador_tea import calibrar_ttea
from controle_mediapipe import sensores

pygame.init()
pygame.mixer.init()

LARGURA, ALTURA = 800, 600
TELA = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("HerPULEs")
clock = pygame.time.Clock()
retangulo_tela = pygame.Rect(0, 400, LARGURA, ALTURA/3)

# --- FONTES E TEXTOS ---
fonte_jogo = pygame.font.Font('fontes/8BIT.TTF', 30)
fonte_contagem = pygame.font.Font('fontes/8BIT.TTF', 100)
fonte_titulo = pygame.font.Font('fontes/DIOGENES.ttf', 100)
texto_titulo = fonte_titulo.render('HerPULEs', True, (204, 51, 0))

fonte_gameover = pygame.font.Font('fontes/8BIT.TTF', 80)
texto_gameover = fonte_gameover.render('GAME OVER', True, (0, 0, 0))
texto_rect = texto_gameover.get_rect(center=(LARGURA//2, ALTURA//4))

# botões
botao_iniciar = pygame.image.load("Imagens/iniciar.png").convert_alpha()
botao_iniciar = pygame.transform.scale(botao_iniciar, (200, 80))
botao_rect = botao_iniciar.get_rect(center=(LARGURA / 2, ALTURA - 70))


# Botão de pular
botao_pular = pygame.image.load("Imagens/pular.png").convert_alpha()
botao_pular = pygame.transform.scale(botao_pular, (250, 100))  
botao_pular_rect = botao_pular.get_rect(center=(LARGURA / 2 + 200, ALTURA - 70))  # Centralizado e mais à direita

# Botão de abaixar
botao_abaixar = pygame.image.load("Imagens/abaixar.png").convert_alpha()
botao_abaixar = pygame.transform.scale(botao_abaixar, (250, 100))  
botao_abaixar_rect = botao_abaixar.get_rect(center=(LARGURA / 2 - 200, ALTURA - 70))  # Centralizado e mais à esquerda

botao_reiniciar = pygame.image.load("Imagens/reiniciar.png").convert_alpha()
botao_reiniciar = pygame.transform.scale(botao_reiniciar, (200, 100))
botao_reiniciar_rect = botao_reiniciar.get_rect(center=(LARGURA // 2,  ALTURA // 2 + 5))

# contagem regressiva
contagem_numero = 3
contagem_timer = pygame.USEREVENT + 2
ultimo_numero_contagem = 0

fundo = pygame.image.load('Imagens/fundo.jpg').convert()
fundo = pygame.transform.scale(fundo, (LARGURA, ALTURA))
fundo.set_alpha(150)

imagem_menu = pygame.image.load('Imagens/herpules.png').convert_alpha()
imagem_menu = pygame.transform.scale(imagem_menu, (LARGURA//2, ALTURA//2))
fundo.set_alpha(150)
# ----------------------------------------

grupo_jogador = pygame.sprite.GroupSingle()
hercules = Hercules(pos=(70, 400))
grupo_jogador.add(hercules)

grupo_obstaculos = pygame.sprite.Group()

chao = Chao(y_pos=400, vel=5)
ceu = Ceu(vel=2, largura_tela=LARGURA)

pygame.mixer.music.load('sons/musica.mp3')
pygame.mixer.music.play(-1)
music_volume = 0.8
pygame.mixer.music.set_volume(music_volume)

som_morte = pygame.mixer.Sound('sons/morte.wav')
som_morte.set_volume(0.3)

pulo = pygame.mixer.Sound('sons/pulo.wav')
pulo.set_volume(0.3)

SPAWN_OBSTACULO = pygame.USEREVENT + 1
pygame.time.set_timer(SPAWN_OBSTACULO, 2000)

# --- FUNÇÕES ---
def checar_colisao():
    if pygame.sprite.spritecollide(grupo_jogador.sprite, grupo_obstaculos, False, pygame.sprite.collide_mask):
        som_morte.play()
        return False
    return True

def desenhar_tela_base():
    """Desenha os elementos que aparecem em quase todas as telas."""
    TELA.blit(fundo, (0, 0))
    ceu.draw(TELA)
    grupo_jogador.draw(TELA)
    pygame.draw.rect(TELA, (0, 0, 0), retangulo_tela)
    chao.draw(TELA)

def desenhar_tela_menu():
    TELA.blit(fundo, (0, 0))
    ceu.draw(TELA)
    
    imagem_menu_rect = imagem_menu.get_rect(center=(LARGURA / 2, ALTURA / 3)) # Ajuste ALTURA / 3 se quiser mais para cima
    TELA.blit(imagem_menu, imagem_menu_rect) # Desenha a imagem na posição calculada
    grupo_jogador.draw(TELA)
    pygame.draw.rect(TELA, (0, 0, 0), retangulo_tela)
    chao.draw(TELA)


def identificar_pe(pose, superficie):
    x, y = pose.get_feet_center()
    if x is not None and y is not None:
        tamanho = 70  # tamanho do quadrado
        rect = pygame.Rect(int(x - tamanho/2), int(y - tamanho/2), tamanho, tamanho)
        pygame.draw.rect(superficie, (255, 128, 0), rect)

def desenhar_score():
    texto = fonte_jogo.render(f"{score:05d}", True, (255, 128, 0))
    TELA.blit(texto, (LARGURA - texto.get_width() - 20, 20))



# --- ADICIONAR AQUI ---
estado_jogo = 'menu'  # O estado inicial do jogo

rodando = True
pose = sensores.Sensores()
cap = cv.VideoCapture(0)

score = 0
score_timer = pygame.USEREVENT + 5
pygame.time.set_timer(score_timer, 1000)  

while rodando:
    hercules_morto = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_c:
                calibrar_ttea()

        if estado_jogo == 'jogando':
            if event.type == SPAWN_OBSTACULO:
                grupo_obstaculos.add(Obstaculo(vel=5, largura_tela=LARGURA, altura_chao=400))
            if event.type == score_timer:
                score += 1

        elif estado_jogo == 'contagem':
            if event.type == contagem_timer:
                contagem_numero -= 1
        

    # Lógica Mediapipe

    ret, frame = cap.read()
    frame = cv.flip(frame, 1)
    frame = pose.scan_feets(frame)
    cv.imshow('Herpules', frame)

    # --- LÓGICA E DESENHO ---
    # Dentro do loop principal, onde você já está detectando os cliques nos botões

    if estado_jogo == 'menu':

        hercules_normal = pygame.image.load("Imagens/hercules-parado.png").convert_alpha()
        altura = hercules_normal.get_height() * 3
        largura = hercules_normal.get_width() * 3
        hercules_normal = pygame.transform.scale(hercules_normal, (largura, altura))
        grupo_jogador.sprite.image = hercules_normal
        grupo_jogador.sprite.rect = grupo_jogador.sprite.image.get_rect(midbottom=(70, 400))
        grupo_jogador.sprite.mask = pygame.mask.from_surface(grupo_jogador.sprite.image)
        grupo_jogador.sprite.vel_y = 0
        grupo_jogador.sprite.no_chao = True
        grupo_jogador.sprite.esta_abaixado = False

        desenhar_tela_menu()

        # Desenha o botão imagem
        TELA.blit(botao_iniciar, botao_rect)

        if botao_rect.collidepoint((pose.feet_x, pose.feet_y)):
            estado_jogo = 'contagem'
            contagem_numero = 3
            pygame.time.set_timer(contagem_timer, 1000)

    elif estado_jogo == 'contagem':
        desenhar_tela_base()

        tempo_atual = pygame.time.get_ticks()
        if tempo_atual - ultimo_numero_contagem > 1000:
            ultimo_numero_contagem = tempo_atual

        if tempo_atual - ultimo_numero_contagem < 700:
            texto_contagem = fonte_contagem.render(str(contagem_numero), True, 'black')
            texto_contagem_rect = texto_contagem.get_rect(center=(LARGURA / 2 , ALTURA / 3 ))
            TELA.blit(texto_contagem, texto_contagem_rect)

        if contagem_numero < 1:
            estado_jogo = 'jogando'
            grupo_obstaculos.empty()
            pygame.time.set_timer(contagem_timer, 0)

            TELA.blit(botao_pular, botao_pular_rect)
            TELA.blit(botao_abaixar, botao_abaixar_rect)

            # Detecta clique no botão pular
            if botao_pular_rect.collidepoint((pose.feet_x, pose.feet_y)) and grupo_jogador.sprite.no_chao:
                grupo_jogador.sprite.vel_y = grupo_jogador.sprite.forca_pulo
                grupo_jogador.sprite.no_chao = False
                pulo.play()
                

            # Detecta clique no botão abaixar
            if botao_abaixar_rect.collidepoint((pose.feet_x, pose.feet_y)):
                grupo_jogador.sprite.esta_abaixado = True
            else:
                grupo_jogador.sprite.esta_abaixado = False

    elif estado_jogo == 'jogando':

        keys = pygame.key.get_pressed()
        grupo_jogador.update(keys)
        grupo_obstaculos.update()
        chao.update()
        ceu.update()

        desenhar_tela_base()
        grupo_obstaculos.draw(TELA)
        desenhar_score()

        
        TELA.blit(botao_pular, botao_pular_rect)
        TELA.blit(botao_abaixar, botao_abaixar_rect)

        # Detecta clique no botão pular
        if botao_pular_rect.collidepoint((pose.feet_x, pose.feet_y)) and grupo_jogador.sprite.no_chao:
            grupo_jogador.sprite.vel_y = grupo_jogador.sprite.forca_pulo
            grupo_jogador.sprite.no_chao = False
            pulo.play()
    
        # Detecta clique no botão abaixar
        if botao_abaixar_rect.collidepoint((pose.feet_x, pose.feet_y)):
            grupo_jogador.sprite.esta_abaixado = True
        else:
            grupo_jogador.sprite.esta_abaixado = False

        if not checar_colisao() and not hercules_morto:
            hercules_morto = True
            som_morte.play()
            estado_jogo = 'game_over'

    elif estado_jogo == 'game_over':
            score = 0

            # 1. Desenha a tela base (céu, chão, etc)
            desenhar_tela_base() 

            grupo_jogador.sprite.image = grupo_jogador.sprite.imagem_morto
     
            grupo_obstaculos.draw(TELA)
            grupo_jogador.draw(TELA)

            TELA.blit(texto_gameover, texto_rect) 
            
            TELA.blit(botao_reiniciar, botao_reiniciar_rect)
            if botao_reiniciar_rect.collidepoint((pose.feet_x, pose.feet_y)):
                estado_jogo = 'contagem'

    identificar_pe(pose, TELA)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
