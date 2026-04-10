import pygame
from model import GameModel
from view import GameView
from input_providers import KeyboardInputProvider, ScriptedInputProvider, MediapipeInputProvider

modo_input = "mediapipe"

class GameController:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()

        self.largura = 800
        self.altura = 600
        self.fps = 60
        self.clock = pygame.time.Clock()
        self.running = True

        self.view = GameView(self.largura, self.altura)

        if modo_input == "teclado":
            self.input_provider = KeyboardInputProvider()
        elif modo_input == "script":
            self.input_provider = ScriptedInputProvider()
        elif modo_input == "mediapipe":
            self.input_provider = MediapipeInputProvider()
        else:
            self.input_provider = KeyboardInputProvider()

        self.pulo_solicitado = False
        self.aga_solicitado = False

        self.evento_score = pygame.USEREVENT + 1
        self.evento_obstaculo = pygame.USEREVENT + 2
        self.evento_contagem = pygame.USEREVENT + 3
        self.evento_calibracao = pygame.USEREVENT + 4

        pygame.time.set_timer(self.evento_score, 1000)

        if modo_input == "mediapipe":
            self.tempo_spawn_obstaculo = 2000
            self.velocidade_obstaculo = 4
        else:
            self.tempo_spawn_obstaculo = 2000
            self.velocidade_obstaculo = 5

        self.model = GameModel(self.largura, self.altura, self.velocidade_obstaculo)
        pygame.time.set_timer(self.evento_obstaculo, self.tempo_spawn_obstaculo)
            
        self.som_pulo = pygame.mixer.Sound("sons/pulo.wav")
        self.som_colisao = pygame.mixer.Sound("sons/morte.wav")

    def processar_eventos(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.KEYDOWN:
                self.processar_keydown(event)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.processar_mouse(event)

            elif event.type == self.evento_score:
                if self.model.estado == "jogando":
                    self.model.score += 1

            elif event.type == self.evento_obstaculo:
                if self.model.estado == "jogando":
                    self.model.adicionar_obstaculo()

            elif event.type == self.evento_contagem:
                self.processar_contagem()

            elif event.type == self.evento_calibracao:
                if self.model.estado == "calibracao":
                    self.input_provider.calibrar()
                    self.model.iniciar_jogo()
                    pygame.time.set_timer(self.evento_calibracao, 0)
                    pygame.time.set_timer(self.evento_contagem, 1000)

    def processar_keyup(self, event):
        if self.model.estado == "jogando" and event.key == pygame.K_UP:
            self.pulo_solicitado = True

    def processar_keydown(self, event):
        if self.model.estado == "jogando" and event.key == pygame.K_DOWN:
            self.aga_solicitado = True

    def processar_mouse(self, event):
        if self.model.estado == "menu":
            if self.view.rect_botao_iniciar.collidepoint(event.pos):
                self.model.iniciar_calibracao()
                pygame.time.set_timer(self.evento_calibracao, 2000)

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