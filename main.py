import pygame
import sys
from model import GameModel
from view import GameView

pygame.init()
pygame.mixer.init()

# Sons
pulo_som = pygame.mixer.Sound('sons/pulo.wav')
pulo_som.set_volume(0.3)
som_morte = pygame.mixer.Sound('sons/morte.wav')
som_morte.set_volume(0.3)
pygame.mixer.music.load('sons/musica.mp3')
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.8)

class GameController:
    def __init__(self):
        self.LARGURA = 800
        self.ALTURA = 600
        
        self.view = GameView(self.LARGURA, self.ALTURA)
        
        self.model = GameModel(self.LARGURA, self.ALTURA)
        
        self.clock = pygame.time.Clock()
        
        self.SPAWN_OBSTACULO = pygame.USEREVENT + 1
        self.SCORE_TIMER = pygame.USEREVENT + 2
        self.CONTAGEM_TIMER = pygame.USEREVENT + 3
        
        pygame.time.set_timer(self.SPAWN_OBSTACULO, 2000)
        pygame.time.set_timer(self.SCORE_TIMER, 1000)

    def run(self):
        ultimo_numero_contagem = 0
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        # Pulo
                        if self.model.hercules.no_chao and self.model.estado == 'jogando':
                            self.model.hercules.vel_y = self.model.hercules.forca_pulo
                            self.model.hercules.no_chao = False
                            pulo_som.play()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if self.model.estado == 'menu':
                        if self.view.rect_botao_iniciar.collidepoint(pos):
                            self.model.iniciar_jogo()
                            pygame.time.set_timer(self.CONTAGEM_TIMER, 1000)
                    elif self.model.estado == 'game_over':
                        if self.view.rect_botao_reiniciar.collidepoint(pos):
                            self.model.resetar_jogo()
                            pygame.time.set_timer(self.CONTAGEM_TIMER, 1000)

                if self.model.estado == 'jogando':
                    if event.type == self.SPAWN_OBSTACULO:
                        self.model.adicionar_obstaculo()
                    if event.type == self.SCORE_TIMER:
                        self.model.score += 1
                
                elif self.model.estado == 'contagem':
                    if event.type == self.CONTAGEM_TIMER:
                        self.model.contagem_numero -= 1
                        if self.model.contagem_numero < 0:
                            self.model.estado = 'jogando'
                            self.model.grupo_obstaculos.empty()
                            pygame.time.set_timer(self.CONTAGEM_TIMER, 0)

            keys = pygame.key.get_pressed()
            
            resultado = self.model.update(keys)
            
            if resultado == "colisao": 
                self.model.estado = 'game_over'
                som_morte.play()

            self.view.desenhar(self.model)
            
            self.clock.tick(60)

if __name__ == "__main__":
    game = GameController()
    game.run()