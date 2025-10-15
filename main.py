import pygame
from entidades.hercules import Hercules
from entidades.chao import Chao
from entidades.ceu import Ceu

pygame.init()

# Configurações da tela
LARGURA, ALTURA = 800, 600
TELA = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("HerPULEs")

clock = pygame.time.Clock()

# Criar jogador
hercules = Hercules(pos=(100, 504))
grupo = pygame.sprite.GroupSingle(hercules)

# Criar chão
chao = Chao(y_pos=510, vel=5)

#Criar o céu
ceu = Ceu(vel=2, largura_tela=LARGURA)

# Loop principal
rodando = True
while rodando:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = False

    keys = pygame.key.get_pressed()
    grupo.update(keys)
    chao.update()
    ceu.update()

    # Desenho
    TELA.fill((135, 206, 235))  # Céu
    ceu.draw(TELA)
    chao.draw(TELA)
    grupo.draw(TELA)
    

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
