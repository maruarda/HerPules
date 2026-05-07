import pygame
from model import GameModel
from view import GameView
from input_providers import KeyboardInputProvider, ScriptedInputProvider, MediapipeInputProvider
from paths import resource_path

MODO_INPUT = 'mediapipe'  # 'teclado', 'script' ou 'mediapipe'

class GameController:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()

        self.largura = 800
        self.altura = 600
        self.fps = 60
        self.clock = pygame.time.Clock()
        self.running = True
        self.pode_iniciar = True

        self.view = GameView(self.largura, self.altura)

        if MODO_INPUT == "teclado":
            self.input_provider = KeyboardInputProvider()
        elif MODO_INPUT == "script":
            self.input_provider = ScriptedInputProvider()
        elif MODO_INPUT == "mediapipe":
            self.input_provider = MediapipeInputProvider()
        else:
            self.input_provider = KeyboardInputProvider()

        self.pulo_solicitado = False
        self.aga_solicitado = False

        self.evento_obstaculo = pygame.USEREVENT + 2
        self.evento_contagem = pygame.USEREVENT + 3
        self.evento_calibracao = pygame.USEREVENT + 4

        if MODO_INPUT == "mediapipe":
            self.tempo_spawn_obstaculo = 2000
            self.velocidade_obstaculo = 4
        else:
            self.tempo_spawn_obstaculo = 2000
            self.velocidade_obstaculo = 5

        self.model = GameModel(self.largura, self.altura, self.velocidade_obstaculo)
        pygame.time.set_timer(self.evento_obstaculo, self.tempo_spawn_obstaculo)

        pygame.mixer.music.load(resource_path('sons/musica.mp3'))
        pygame.mixer.music.play(-1)
        music_volume = 0.4
        pygame.mixer.music.set_volume(music_volume)

        self.som_pulo = pygame.mixer.Sound(resource_path("sons/pulo.wav"))
        self.som_colisao = pygame.mixer.Sound(resource_path("sons/morte.wav"))

    def processar_eventos(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.KEYDOWN:
                self.processar_keydown(event)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.processar_mouse(event)

            elif event.type == self.evento_obstaculo:
                if self.model.estado == "jogando":
                    self.model.adicionar_obstaculo()

            elif event.type == self.evento_contagem:
                self.processar_contagem()

            elif event.type == self.evento_calibracao:
                if self.model.estado == "calibracao":
                    if hasattr(self.input_provider, "calibrar"):
                        self.input_provider.calibrar()
                    self.model.iniciar_jogo()
                    pygame.time.set_timer(self.evento_calibracao, 0)
                    pygame.time.set_timer(self.evento_contagem, 1000)

    def processar_keydown(self, event):
        if self.model.estado == "jogando":
            if event.key == pygame.K_UP:
                self.pulo_solicitado = True
            elif event.key == pygame.K_DOWN:
                self.aga_solicitado = True

    def processar_mouse(self, event):
        if MODO_INPUT == "mediapipe":
            return

        if self.model.estado == "menu":
            if self.view.rect_botao_iniciar.collidepoint(event.pos):
                if MODO_INPUT == "mediapipe":
                    self.model.iniciar_calibracao()
                    pygame.time.set_timer(self.evento_calibracao, 2000)
                else:
                    self.model.iniciar_jogo()
                    pygame.time.set_timer(self.evento_contagem, 1000)

        elif self.model.estado == "game_over":
            if self.view.rect_botao_reiniciar.collidepoint(event.pos):
                self.model.resetar_jogo()
                pygame.time.set_timer(self.evento_contagem, 0)
                pygame.time.set_timer(self.evento_calibracao, 0)
                self.pulo_solicitado = False
                self.aga_solicitado = False

    def processar_contagem(self):
        if self.model.estado == "contagem":
            self.model.contagem_numero -= 1

            if self.model.contagem_numero <= 0:
                self.model.estado = "jogando"
                pygame.time.set_timer(self.evento_contagem, 0)

    def atualizar(self):
        input_atual = self.input_provider.get_input()

        if self.pulo_solicitado:
            input_atual.pular = True

        if input_atual.pular and self.model.estado == "jogando" and self.model.hercules.no_chao:
            self.som_pulo.play()

        if self.aga_solicitado:
            input_atual.abaixar = True

        if self.model.estado == "menu" and MODO_INPUT == "mediapipe":
            if input_atual.pular and self.pode_iniciar:
                self.model.iniciar_calibracao()
                pygame.time.set_timer(self.evento_calibracao, 2000)
                self.pode_iniciar = False

        if self.model.estado == "menu":
            self.pode_iniciar = True

        if self.model.estado == "game_over" and MODO_INPUT == "mediapipe":
            if input_atual.pular:
                self.model.resetar_jogo()

        resultado = self.model.update(input_atual)

        if resultado == "colisao":
            self.som_colisao.play()
            self.model.estado = "game_over"
            self.model.hercules.esta_correndo = False
            self.model.hercules.esta_abaixado = False
            self.model.hercules.vel_y = 0

        self.pulo_solicitado = False
        self.aga_solicitado = False

    def run(self):
        while self.running:
            self.processar_eventos()
            self.atualizar()
            self.view.desenhar(self.model)
            self.clock.tick(self.fps)

        if hasattr(self.input_provider, "release"):
            self.input_provider.release()

        pygame.quit()
