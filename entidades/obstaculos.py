import pygame
import random

class Obstaculo(pygame.sprite.Sprite):
    def __init__(self, vel, largura_tela, altura_chao):
        super().__init__()

     
        tipos_de_obstaculos = [
            'Imagens/PeA-juntos.png',
            'Imagens/agonia.png',
            'Imagens/panico.png',
            'Imagens/Sprite-coluna-inteira.png',
            'Imagens/Sprite-coluna-quebrada.png',
            'Imagens/colunas-juntas.png',
            'Imagens/Sprite-vaso.png',
            'Imagens/hades1.png',
            'Imagens/fogo1.gif',
            'Imagens/fogão.png'
        ]

        imagem_escolhida = random.choice(tipos_de_obstaculos)
        if (imagem_escolhida == 'Imagens/PeA-juntos.png') or (imagem_escolhida =='Imagens/agonia.png') or (imagem_escolhida == 'Imagens/panico.png'):
            scale_factor = random.uniform(1.5, 2.2) 
        elif imagem_escolhida == 'Imagens/Sprite-coluna-quebrada.png':
            scale_factor = random.uniform(2, 2.7)
        else:
            scale_factor = random.uniform(2, 2.5) 

        original_image = pygame.image.load(imagem_escolhida).convert_alpha() 
        
        new_width = int(original_image.get_width() * scale_factor)
        new_height = int(original_image.get_height() * scale_factor)
        self.image = pygame.transform.scale(original_image, (new_width, new_height))

        alturas_possiveis = [altura_chao, altura_chao - 85, altura_chao - 90, altura_chao - 100]
        altura_escolhida = random.choice(alturas_possiveis)

        if imagem_escolhida == 'Imagens/hades1.png' or imagem_escolhida == 'Imagens/fogo1.png' or imagem_escolhida == 'Imagens/fogão.png':
            self.rect = self.image.get_rect(bottomleft=(largura_tela + random.randint(200, 300), altura_escolhida))
        else:
            self.rect = self.image.get_rect(bottomleft=(largura_tela + random.randint(200, 300), altura_chao))

        self.mask = pygame.mask.from_surface(self.image)
        
        self.vel = vel

    def update(self):
        self.rect.x -= self.vel

        if self.rect.right < 0:
            self.kill()
