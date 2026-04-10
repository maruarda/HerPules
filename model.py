import pygame
from entidades.hercules import Hercules
from entidades.obstaculos import Obstaculo
from entidades.ceu import Ceu
from entidades.chao import Chao
from entidades.iniciar import Botao


class GameModel:

    def __init__(self, largura, altura, velocidade_obstaculo=5):
        self.largura = largura
        self.altura = altura
        self.velocidade_obstaculo = velocidade_obstaculo
        self.score = 0
        self.estado = 'menu'  # menu, calibracao ,contagem, jogando, game_over, 
        self.contagem_numero = 3

        self.grupo_jogador = pygame.sprite.GroupSingle()
        self.hercules = Hercules(pos=(70, 400))
        self.grupo_jogador.add(self.hercules)

        self.grupo_obstaculos = pygame.sprite.Group()
        self.chao = Chao(y_pos=400, vel=5)
        self.ceu = Ceu(vel=2, largura_tela=largura)

    def iniciar_jogo(self):
        self.estado = 'contagem'
        self.contagem_numero = 3

    def iniciar_calibracao(self):
        self.estado = 'calibracao'

    def resetar_jogo(self):
        self.score = 0
        self.grupo_obstaculos.empty()
        self.hercules.rect.midbottom = (70, 400)
        self.hercules.vel_y = 0
        self.hercules.no_chao = True
        self.hercules.image = self.hercules.imagem_parado
        self.hercules.esta_abaixado = False
        self.hercules.esta_correndo = False
        self.hercules.anim_index = 0
        self.estado = 'menu'
        self.contagem_numero = 3

    def adicionar_obstaculo(self):
        distancia_minima = 300  # teste 300, 350 ou 400

        if len(self.grupo_obstaculos) > 0:
            ultimo = max(self.grupo_obstaculos, key=lambda obs: obs.rect.x)

            if ultimo.rect.x > self.largura - distancia_minima:
                return

        obs = Obstaculo(vel=5, largura_tela=self.largura, altura_chao=400)
        self.grupo_obstaculos.add(obs)

    def update(self, input_state):
        if self.estado == "jogando":
            if input_state.pular:
                self.hercules.pular()

            self.hercules.abaixar(input_state.abaixar)

            self.grupo_jogador.update()
            self.grupo_obstaculos.update()

            if self.hercules.esta_em_movimento():
                self.ceu.update()
                self.chao.update()

            if pygame.sprite.spritecollide(
                self.hercules,
                self.grupo_obstaculos,
                False,
                pygame.sprite.collide_mask
            ):
                return "colisao"

        elif self.estado in ["menu", "calibracao", "contagem"]:
            self.grupo_jogador.update()

            if self.hercules.esta_em_movimento():
                self.ceu.update()
                self.chao.update()

        elif self.estado == "game_over":
            # não atualiza nada para tudo ficar parado
            pass

        return None
