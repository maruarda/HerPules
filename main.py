# jogo.py

import pygame
import sys
from entidades.hercules import Hercules
from entidades.chao import Chao
from entidades.ceu import Ceu
from entidades.obstaculos import Obstaculo

pygame.init()
pygame.mixer.init()

# Configurações da tela
LARGURA, ALTURA = 800, 600
TELA = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("HerPULEs")
clock = pygame.time.Clock()

# --- FONTES E TEXTOS ---
fonte = pygame.font.Font(None, 50)
texto_inicio = fonte.render("Pressione qualquer tecla para comecar", True, "White")
texto_rect = texto_inicio.get_rect(center=(LARGURA / 2, ALTURA / 2))

# --- IMAGENS ---
fundo = pygame.image.load('Imagens/Fundo.jpg').convert()
fundo = pygame.transform.scale(fundo, (LARGURA, ALTURA))
fundo.set_alpha(150) # Deixei um pouco mais visível, ajuste se quiser

# --- ESTADO DO JOGO ---
jogo_ativo = False

# --- GRUPOS DE SPRITES ---
# <<< CORREÇÃO: Removi o jogador duplicado. Agora só existe um.
grupo_jogador = pygame.sprite.GroupSingle()
hercules = Hercules(pos=(100, 510))
grupo_jogador.add(hercules)

grupo_obstaculos = pygame.sprite.Group()

# --- ENTIDADES DO CENÁRIO ---
chao = Chao(y_pos=510, vel=5)
ceu = Ceu(vel=2, largura_tela=LARGURA)

#música de fundo
pygame.mixer.music.load('sons/musica.mp3')
pygame.mixer.music.play(-1)
music_volume = 0.2
pygame.mixer.music.set_volume(music_volume)

# --- TIMERS ---
SPAWN_OBSTACULO = pygame.USEREVENT + 1
pygame.time.set_timer(SPAWN_OBSTACULO, 2000) # Obstáculos a cada 2 segundos

# --- FUNÇÕES ---
def checar_colisao():
    # A colisão por máscara é mais precisa que a por retângulo
    if pygame.sprite.spritecollide(grupo_jogador.sprite, grupo_obstaculos, False, pygame.sprite.collide_mask):
        return False # <<< MUDANÇA: Retorna False para parar o jogo
    return True # <<< MUDANÇA: Retorna True para continuar

# --- LOOP PRINCIPAL ---
rodando = True
while rodando:
    # --- EVENTOS ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = False
        
        # <<< LÓGICA CORRIGIDA: Trata os eventos dependendo do estado do jogo
        if jogo_ativo:
            # Evento para criar obstáculos SÓ acontece se o jogo estiver ativo
            if event.type == SPAWN_OBSTACULO:
                grupo_obstaculos.add(Obstaculo(vel=5, largura_tela=LARGURA, altura_chao=510))
        else:
            # Evento para começar o jogo SÓ é verificado se o jogo NÃO estiver ativo
            if event.type == pygame.KEYDOWN:
                jogo_ativo = True
                grupo_obstaculos.empty() # Limpa os obstáculos da tela anterior

    # --- LÓGICA E DESENHO ---
    if jogo_ativo:
        # --- ATUALIZAÇÕES (UPDATE) ---
        keys = pygame.key.get_pressed()
        grupo_jogador.update(keys)
        grupo_obstaculos.update()
        chao.update()
        ceu.update()
        
        # Verifica colisões e atualiza o estado do jogo
        jogo_ativo = checar_colisao()

        # --- DESENHO (DRAW) ---
        # <<< ORDEM CORRIGIDA: Desenha do mais distante para o mais próximo
        TELA.blit(fundo, (0, 0))
        ceu.draw(TELA)
        chao.draw(TELA)
        grupo_obstaculos.draw(TELA)
        grupo_jogador.draw(TELA)

    else: # Tela de início "congelada"
        TELA.blit(fundo, (0, 0))
        ceu.draw(TELA)
        chao.draw(TELA)
        grupo_jogador.draw(TELA) # Mostra o jogador parado
        TELA.blit(texto_inicio, texto_rect) # Mensagem por cima de tudo

    # --- ATUALIZAÇÃO FINAL DA TELA ---
    pygame.display.flip()
    clock.tick(60)

# --- FIM DO JOGO ---
pygame.quit()
sys.exit()