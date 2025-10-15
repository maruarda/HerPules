import pygame
from entidades.hercules import Hercules
from entidades.chao import Chao

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

# Criar chão
chao = Chao(y_pos=510, vel=5)

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


    pygame.display.flip()
    clock.tick(60)

pygame.quit()