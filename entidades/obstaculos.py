import pygame
import random

class Obstaculo(pygame.sprite.Sprite):
    def __init__(self, vel, largura_tela, altura_chao):
        super().__init__()

        tipos_de_obstaculos = [
            'Imagens/agonia.png', 
            'Imagens/panico.png', 
            'Imagens/PeA-juntos.png', 
            'Imagens/Sprite-coluna-inteira.png', 
            'Imagens/Sprite-coluna-quebrada.png'

        ]

        imagem_escolhida = random.choice(tipos_de_obstaculos)
        self.image = pygame.image.load(imagem_escolhida).convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.image.get_height() * 3, self.image.get_width() * 3)) 

        self.rect = self.image.get_rect(bottomleft=(largura_tela + random.randint(200, 300), altura_chao))

        self.mask = pygame.mask.from_surface(self.image)
        
        self.vel = vel

    def update(self):
        self.rect.x -= self.vel

        if self.rect.right < 0:
            self.kill()
