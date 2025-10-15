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

# Fonte para a mensagem de início
fonte = pygame.font.Font(None, 50)
texto_inicio = fonte.render("Pressione qualquer tecla para comecar", True, "White")
texto_rect = texto_inicio.get_rect(center = (LARGURA / 2, ALTURA / 2))


clock = pygame.time.Clock()

fundo = pygame.image.load('Imagens\Fundo.jpg').convert()
fundo = pygame.transform.scale(fundo, (LARGURA, ALTURA))
fundo.set_alpha(100)

#Variável para controlar o estado do jogo
jogo_ativo = False

# Criar jogador
hercules = Hercules(pos=(100, 510)) # Posição ajustada para o chao
grupo = pygame.sprite.GroupSingle(hercules)
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
        #Verifica se o jogo NÃO está ativo e se uma tecla foi pressionada
        if not jogo_ativo:
            if event.type == pygame.KEYDOWN:
                jogo_ativo = True

    # Lógica principal do jogo só executa se jogo_ativo for True
    if jogo_ativo:
        keys = pygame.key.get_pressed()
        grupo.update(keys)
        chao.update()

        # Desenho do jogo ativo
        TELA.blit(fundo, (0, 0))
        chao.draw(TELA)
        grupo.draw(TELA)
    else:
        #Tela de início congelada
        TELA.blit(fundo, (0, 0)) 
        chao.draw(TELA)
        grupo.draw(TELA)
        TELA.blit(texto_inicio, texto_rect)

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
pygame.quit()
sys.exit()
