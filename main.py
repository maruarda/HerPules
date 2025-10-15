import pygame
import sys
from entidades.hercules import Hercules
from entidades.chao import Chao
from entidades.ceu import Ceu
from entidades.obstaculos import Obstaculo 
pygame.init()

# Configurações da tela
LARGURA, ALTURA = 800, 600
TELA = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("HerPULEs")

clock = pygame.time.Clock()

#Criar jogador
hercules = Hercules(pos=(100, 504))
grupo_jogador = pygame.sprite.GroupSingle(hercules)
grupo_obstaculos = pygame.sprite.Group()

# Criar chão e céu
chao = Chao(y_pos=510, vel=5)
ceu = Ceu(vel=2, largura_tela=LARGURA)


SPAWN_OBSTACULO = pygame.USEREVENT + 1
pygame.time.set_timer(SPAWN_OBSTACULO, 3500) #cada milisegundos acontece


def checar_colisao():
    if pygame.sprite.spritecollide(grupo_jogador.sprite, grupo_obstaculos, False, pygame.sprite.collide_mask):
        return True 
    return False 

# Loop principal
rodando = True
while rodando:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = False

        if event.type == SPAWN_OBSTACULO:
            grupo_obstaculos.add(Obstaculo(vel=5, largura_tela=LARGURA, altura_chao=510))

    TELA.fill((135, 206, 235))  
    keys = pygame.key.get_pressed()
    grupo_jogador.update(keys)
    chao.update()
    ceu.update()
    grupo_obstaculos.update() # 

    # Desenho
    ceu.draw(TELA)
    chao.draw(TELA)
    grupo_jogador.draw(TELA)
    grupo_obstaculos.draw(TELA) 

 
    if checar_colisao():
        rodando = False 

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
