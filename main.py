# main.py

import pygame
import sys
from entidades.hercules import Hercules
from entidades.chao import Chao
from entidades.ceu import Ceu
from entidades.obstaculos import Obstaculo
from entidades.iniciar import Botao
from controle_mediapipe.sensores import FootButtonController, ROI  # Mediapipe

pygame.init()
pygame.mixer.init()

# --- CONFIGURAÇÕES DA JANELA ---
LARGURA, ALTURA = 800, 600
TELA = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("HerPULEs")
clock = pygame.time.Clock()
retangulo_tela = pygame.Rect(0, 400, LARGURA, ALTURA / 3)

# --- FONTES E TEXTOS ---
fonte_jogo = pygame.font.Font('fontes/8BIT.ttf', 30)
fonte_contagem = pygame.font.Font('fontes/8BIT.ttf', 100)
fonte_titulo = pygame.font.Font('fontes/DIOGENES.ttf', 100)
texto_titulo = fonte_titulo.render('HerPULEs', True, (204, 51, 0))
texto_jogue = fonte_jogo.render('Jogue aqui!', True, 'white')
texto_jogue.set_alpha(100)
texto_jogue_rect = texto_jogue.get_rect(center=(LARGURA / 3, ALTURA - 75))

# --- ESTADOS DO JOGO ---
estado_jogo = 'menu'

# --- CONTAGEM REGRESSIVA ---
contagem_numero = 3
contagem_timer = pygame.USEREVENT + 2
ultimo_numero_contagem = 0

# --- IMAGENS E SOM ---
fundo = pygame.image.load('Imagens/Fundo.jpg').convert()
fundo = pygame.transform.scale(fundo, (LARGURA, ALTURA))
fundo.set_alpha(150)

pygame.mixer.music.load('sons/musica.mp3')
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.8)
som_morte = pygame.mixer.Sound('sons/morte.wav')
som_morte.set_volume(0.3)

# --- ENTIDADES ---
grupo_jogador = pygame.sprite.GroupSingle()
hercules = Hercules(pos=(70, 400))
grupo_jogador.add(hercules)
grupo_obstaculos = pygame.sprite.Group()
chao = Chao(y_pos=400, vel=5)
ceu = Ceu(vel=2, largura_tela=LARGURA)

SPAWN_OBSTACULO = pygame.USEREVENT + 1
pygame.time.set_timer(SPAWN_OBSTACULO, 2000)

# --- BOTÕES PROJETADOS NO CHÃO (PULAR E AGACHAR) ---
BTN_SIZE = 160
BTN_CROUCH_RECT = pygame.Rect(60, ALTURA - BTN_SIZE - 20, BTN_SIZE, BTN_SIZE)
BTN_JUMP_RECT = pygame.Rect(LARGURA - BTN_SIZE - 60, ALTURA - BTN_SIZE - 20, BTN_SIZE, BTN_SIZE)

# --- SENSOR DE PÉS (MEDIAPIPE) ---
foot = FootButtonController(
    cam_index=0,
    jump_roi=ROI(100, 260, 150, 150),
    crouch_roi=ROI(380, 260, 150, 150),
    start_roi=ROI(240, 260, 180, 150),  # área central para "INICIAR"
    show_debug=True
)
foot.start()

# --- CLASSE DE TECLAS VIRTUAIS ---
class KeyProxy:
    def __init__(self):
        self.state = {}
    def __getitem__(self, key):
        return self.state.get(key, False)
keys_proxy = KeyProxy()

# --- FUNÇÕES AUXILIARES ---
def checar_colisao():
    if pygame.sprite.spritecollide(grupo_jogador.sprite, grupo_obstaculos, False, pygame.sprite.collide_mask):
        som_morte.play()
        return False
    return True

def desenhar_tela_base():
    TELA.blit(fundo, (0, 0))
    ceu.draw(TELA)
    grupo_jogador.draw(TELA)
    pygame.draw.rect(TELA, (0, 0, 0), retangulo_tela)
    chao.draw(TELA)
    TELA.blit(texto_jogue, texto_jogue_rect)

# --- LOOP PRINCIPAL ---
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

    # --- ESTADOS DO JOGO ---
    if estado_jogo == 'menu':
        desenhar_tela_base()

        # título
        texto_titulo = fonte_titulo.render('HerPULEs!', True, (204, 122, 0))
        TELA.blit(texto_titulo, (LARGURA / 2 - texto_titulo.get_width() / 2, ALTURA / 4))

        # botão de INICIAR projetado no chão
        BTN_START_RECT = pygame.Rect(LARGURA / 2 - 150, ALTURA - 200, 300, 120)
        pygame.draw.rect(TELA, (30, 30, 30), BTN_START_RECT, border_radius=25)
        cor_borda = (0, 255, 0) if foot.start_hold else (0, 150, 0)
        pygame.draw.rect(TELA, cor_borda, BTN_START_RECT, width=6, border_radius=25)
        label_s = fonte_jogo.render("INICIAR", True, cor_borda)
        TELA.blit(label_s, (BTN_START_RECT.centerx - label_s.get_width() // 2,
                            BTN_START_RECT.centery - label_s.get_height() // 2))

        # inicia o jogo quando os dois pés estão sobre o botão
        if foot.start_hold:
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
            texto_contagem_rect = texto_contagem.get_rect(center=(LARGURA / 2, ALTURA / 3))
            TELA.blit(texto_contagem, texto_contagem_rect)

        if contagem_numero < 1:
            estado_jogo = 'jogando'
            grupo_obstaculos.empty()
            pygame.time.set_timer(contagem_timer, 0)

    elif estado_jogo == 'jogando':
        # atualiza estado dos pés
        keys_proxy.state[pygame.K_UP] = foot.pop_jump()
        keys_proxy.state[pygame.K_DOWN] = foot.crouching

        grupo_jogador.update(keys_proxy)
        grupo_obstaculos.update()
        chao.update()
        ceu.update()

        desenhar_tela_base()
        grupo_obstaculos.draw(TELA)

        # botões de chão (pular e agachar)
        pygame.draw.rect(TELA, (30, 30, 30), BTN_CROUCH_RECT, border_radius=30)
        pygame.draw.rect(TELA, (255, 150, 0), BTN_CROUCH_RECT, width=6, border_radius=30)
        label_c = fonte_jogo.render("AGACHAR", True, (255, 150, 0))
        TELA.blit(label_c, (BTN_CROUCH_RECT.centerx - label_c.get_width() // 2,
                            BTN_CROUCH_RECT.centery - label_c.get_height() // 2))

        pygame.draw.rect(TELA, (30, 30, 30), BTN_JUMP_RECT, border_radius=30)
        pygame.draw.rect(TELA, (0, 200, 255), BTN_JUMP_RECT, width=6, border_radius=30)
        label_j = fonte_jogo.render("PULAR", True, (0, 200, 255))
        TELA.blit(label_j, (BTN_JUMP_RECT.centerx - label_j.get_width() // 2,
                            BTN_JUMP_RECT.centery - label_j.get_height() // 2))

        # colisão = volta pro menu
        if not checar_colisao():
            estado_jogo = 'menu'

    pygame.display.flip()
    clock.tick(60)

# --- FINALIZA ---
foot.stop()
pygame.quit()
sys.exit()
