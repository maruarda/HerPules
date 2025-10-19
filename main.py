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
retangulo_tela = pygame.Rect(0, 400, LARGURA, ALTURA/3)

# --- FONTES E TEXTOS ---
fonte_jogo = pygame.font.Font('fontes/8BIT.TTF', 30)
fonte_contagem = pygame.font.Font('fontes/8BIT.TTF', 100)
fonte_titulo = pygame.font.Font('fontes/DIOGENES.ttf', 100)
texto_titulo = fonte_titulo.render('HerPULEs', True, (204, 51, 0))

# botões
botao_iniciar = pygame.image.load("Imagens/iniciar.png").convert_alpha()
botao_iniciar = pygame.transform.scale(botao_iniciar, (200, 80))
botao_rect = botao_iniciar.get_rect(center=(LARGURA / 2, ALTURA - 70))


# Botão de pular
botao_pular = pygame.image.load("Imagens/pular.png").convert_alpha()
botao_pular = pygame.transform.scale(botao_pular, (250, 100))  
botao_pular_rect = botao_pular.get_rect(center=(LARGURA / 2 + 150, ALTURA - 70))  # Centralizado e mais à direita

# Botão de abaixar
botao_abaixar = pygame.image.load("Imagens/abaixar.png").convert_alpha()
botao_abaixar = pygame.transform.scale(botao_abaixar, (250, 100))  
botao_abaixar_rect = botao_abaixar.get_rect(center=(LARGURA / 2 - 150, ALTURA - 70))  # Centralizado e mais à esquerda



# contagem regressiva
contagem_numero = 3
contagem_timer = pygame.USEREVENT + 2
ultimo_numero_contagem = 0

fundo = pygame.image.load('Imagens/fundo.jpg').convert()
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


# --- ADICIONAR AQUI ---
estado_jogo = 'menu'  # O estado inicial do jogo

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
    # Dentro do loop principal, onde você já está detectando os cliques nos botões

    if estado_jogo == 'menu':
        desenhar_tela_base()
        # Desenha o botão imagem
        TELA.blit(botao_iniciar, botao_rect)

        # Detecta clique do mouse
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()[0]

        if botao_rect.collidepoint(mouse_pos) and mouse_click:
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

            mouse_pos = pygame.mouse.get_pos()
            mouse_click = pygame.mouse.get_pressed()[0]


            # Detecta clique no botão pular
            if botao_pular_rect.collidepoint(mouse_pos) and mouse_click:
                grupo_jogador.sprite.vel_y = grupo_jogador.sprite.forca_pulo
                grupo_jogador.sprite.no_chao = False
                pulo.play()
                

            # Detecta clique no botão abaixar
            if botao_abaixar_rect.collidepoint(mouse_pos) and mouse_click:
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
        
        TELA.blit(botao_pular, botao_pular_rect)
        TELA.blit(botao_abaixar, botao_abaixar_rect)

        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()[0]


        # Detecta clique no botão pular
        if botao_pular_rect.collidepoint(mouse_pos) and mouse_click:
            grupo_jogador.sprite.vel_y = grupo_jogador.sprite.forca_pulo
            grupo_jogador.sprite.no_chao = False
            pulo.play()
            
    
        # Detecta clique no botão abaixar
        if botao_abaixar_rect.collidepoint(mouse_pos) and mouse_click:
            grupo_jogador.sprite.esta_abaixado = True
        else:
            grupo_jogador.sprite.esta_abaixado = False

        if not checar_colisao():
            estado_jogo = 'menu'


    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
