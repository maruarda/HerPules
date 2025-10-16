# jogo.py

import pygame
import sys
import os
from entidades.hercules import Hercules
from entidades.chao import Chao
from entidades.ceu import Ceu
from entidades.obstaculos import Obstaculo
from entidades.iniciar import Botao 

pygame.init()
pygame.mixer.init()


LARGURA, ALTURA = 800, 600
TELA = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("HerPULEs")
clock = pygame.time.Clock()

# --- FONTES E TEXTOS ---
fonte_jogo = pygame.font.Font('fontes/8BIT.ttf', 30) 
fonte_contagem = pygame.font.Font('fontes/8BIT.ttf', 100) 

# --- ESTADOS DO JOGO --- # 
estado_jogo = 'menu' 


botao_iniciar = Botao(
    x=(LARGURA / 2) + 200, 
    y=ALTURA - 70, 
    texto='Iniciar', 
    fonte=fonte_jogo
)

# contagem regressiva
contagem_numero = 3
contagem_timer = pygame.USEREVENT + 2 
ultimo_numero_contagem = 0

fundo = pygame.image.load('Imagens/Fundo.jpg').convert()
fundo = pygame.transform.scale(fundo, (LARGURA, ALTURA))
fundo.set_alpha(150) 

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
    chao.draw(TELA)
    grupo_jogador.draw(TELA) 


rodando = True
while rodando:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = False
        
        
        if estado_jogo == 'jogando':
            if event.type == SPAWN_OBSTACULO:
                grupo_obstaculos.add(Obstaculo(vel=5, largura_tela=LARGURA, altura_chao=400))
        
        elif estado_jogo == 'contagem':
            if event.type == contagem_timer:
                contagem_numero -= 1

    # --- LÓGICA E DESENHO ---
    if estado_jogo == 'menu':
        desenhar_tela_base()
        botao_iniciar.draw(TELA)

        if botao_iniciar.check_click():
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
            texto_contagem_rect = texto_contagem.get_rect(center=(LARGURA / 2, ALTURA / 2))
            TELA.blit(texto_contagem, texto_contagem_rect)
        
        if contagem_numero < 1:
            estado_jogo = 'jogando'
            grupo_obstaculos.empty() 
            pygame.time.set_timer(contagem_timer, 0) 

    elif estado_jogo == 'jogando':
        keys = pygame.key.get_pressed()
        grupo_jogador.update(keys)
        grupo_obstaculos.update()
        chao.update()
        ceu.update()
        

        desenhar_tela_base()
        grupo_obstaculos.draw(TELA)
        
        if not checar_colisao():
            estado_jogo = 'menu' 

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()