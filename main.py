# jogo.py

import pygame
import sys
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


fonte = pygame.font.Font(None, 50)
texto_inicio = fonte.render("Pressione qualquer tecla para comecar", True, "White")
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

SPAWN_OBSTACULO = pygame.USEREVENT + 1
pygame.time.set_timer(SPAWN_OBSTACULO, 2000) 

def checar_colisao():
    if pygame.sprite.spritecollide(grupo_jogador.sprite, grupo_obstaculos, False, pygame.sprite.collide_mask):
        return False 
    return True 

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