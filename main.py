# jogo.py

import pygame
import sys
import os
from entidades.hercules import Hercules
from entidades.chao import Chao
from entidades.ceu import Ceu
from entidades.obstaculos import Obstaculo

pygame.init()
pygame.mixer.init()


LARGURA, ALTURA = 800, 600
TELA = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("HerPULEs")
clock = pygame.time.Clock()

# --- FONTES E TEXTOS ---
fonte = pygame.font.Font('fontes/DIOGENES.ttf', 50)
texto_inicio = fonte.render("Pressione qualquer tecla para comecar", True, "black")
texto_rect = texto_inicio.get_rect(center=(LARGURA / 2, ALTURA / 2))


fundo = pygame.image.load('Imagens/Fundo.jpg').convert()
fundo = pygame.transform.scale(fundo, (LARGURA, ALTURA))
fundo.set_alpha(150) 


jogo_ativo = False


grupo_jogador = pygame.sprite.GroupSingle()
hercules = Hercules(pos=(100, 510))
grupo_jogador.add(hercules)

grupo_obstaculos = pygame.sprite.Group()

chao = Chao(y_pos=510, vel=5)
ceu = Ceu(vel=2, largura_tela=LARGURA)

pygame.mixer.music.load('sons/musica.mp3')
pygame.mixer.music.play(-1)
music_volume = 0.2
pygame.mixer.music.set_volume(music_volume)
som_morte = pygame.mixer.Sound('sons/morte.wav')
som_morte.set_volume(0.4)

SPAWN_OBSTACULO = pygame.USEREVENT + 1
pygame.time.set_timer(SPAWN_OBSTACULO, 2000) 

# --- PONTUAÇÃO E RECORDE ---
score = 0
high_score = 0
arquivo_recorde = "highscore.txt"

# Função para carregar o recorde
def carregar_high_score():
    global high_score
    if os.path.exists(arquivo_recorde):
        try:
            with open(arquivo_recorde, 'r') as file:
                high_score = int(file.read())
        except (ValueError, IOError):
            # Se o arquivo estiver corrompido ou vazio, começa com 0
            high_score = 0
    else:
        # Se o arquivo não existe, começa com 0
        high_score = 0

# Função para salvar o recorde
def salvar_high_score():
    with open(arquivo_recorde, 'w') as file:
        file.write(str(int(high_score)))

carregar_high_score()
velocidade_score = 1 # A cada frame, o score aumenta este valor

# --- FUNÇÕES ---
def checar_colisao():
    if pygame.sprite.spritecollide(grupo_jogador.sprite, grupo_obstaculos, False, pygame.sprite.collide_mask):
        som_morte.play()
        return False # <<< MUDANÇA: Retorna False para parar o jogo
    return True # <<< MUDANÇA: Retorna True para continuar

rodando = True
while rodando:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = False
        
        if jogo_ativo:
            if event.type == SPAWN_OBSTACULO:
                grupo_obstaculos.add(Obstaculo(vel=5, largura_tela=LARGURA, altura_chao=510))
        else:
            if event.type == pygame.KEYDOWN:
                jogo_ativo = True
                grupo_obstaculos.empty() 

    # --- LÓGICA E DESENHO ---
    if jogo_ativo:
        keys = pygame.key.get_pressed()
        grupo_jogador.update(keys)
        grupo_obstaculos.update()
        chao.update()
        ceu.update()
        
        jogo_ativo = checar_colisao()

        TELA.blit(fundo, (0, 0))
        ceu.draw(TELA)
        chao.draw(TELA)
        grupo_obstaculos.draw(TELA)
        grupo_jogador.draw(TELA)

    else: 
        TELA.blit(fundo, (0, 0))
        ceu.draw(TELA)
        chao.draw(TELA)
        grupo_jogador.draw(TELA) 
        TELA.blit(texto_inicio, texto_rect) 

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()