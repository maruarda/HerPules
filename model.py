import pygame
from entidades.hercules import Hercules
from entidades.chao import Chao
from entidades.ceu import Ceu
from entidades.obstaculos import Obstaculo

class GameModel:
    def __init__(self, largura, altura):
        self.largura = largura
        self.altura = altura
        self.score = 0
        self.estado = 'menu'  # menu, contagem, jogando, game_over
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

    def resetar_jogo(self):
        self.score = 0
        self.grupo_obstaculos.empty()
        self.hercules.rect.midbottom = (70, 400)
        self.hercules.vel_y = 0
        self.hercules.no_chao = True
        self.hercules.image = self.hercules.imagem_parado
        self.hercules.esta_abaixado = False
        self.hercules.esta_correndo = False
        self.iniciar_jogo()

    def adicionar_obstaculo(self):
        obs = Obstaculo(vel=5, largura_tela=self.largura, altura_chao=400)
        self.grupo_obstaculos.add(obs)

    def update(self, keys):
        if self.estado == 'jogando':
            self.grupo_jogador.update(keys)
            self.grupo_obstaculos.update()
            self.chao.update()
            self.ceu.update()
            
            if pygame.sprite.spritecollide(self.hercules, self.grupo_obstaculos, False, pygame.sprite.collide_mask):
                return "colisao" # Avisa o controller que bateu
        
        elif self.estado == 'menu' or self.estado == 'contagem':
            if self.estado == 'menu':
                 self.hercules.image = self.hercules.imagem_parado
            self.chao.update()
            self.ceu.update()
        
        return None