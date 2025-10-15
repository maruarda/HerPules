import pygame
import random

class Ceu:
    def __init__(self, vel, largura_tela): # Adicionei largura_tela aqui
        self.image = pygame.image.load("Imagens/nuvem.png").convert_alpha() 
        self.image = pygame.transform.scale(self.image, (self.image.get_height() * 3, self.image.get_width() * 3)) 

        self.copias = []
        largura_img = self.image.get_width()

        for i in range(3):
            pos_x = random.randint(0, largura_tela)
            pos_y = random.randint(30, 200)
            rect = self.image.get_rect(topleft=(pos_x, pos_y))
            self.copias.append(rect)

        self.vel = vel

    def update(self):
        for rect in self.copias:
            rect.x -= self.vel

        largura_img = self.image.get_width()
        for rect in self.copias:
            if rect.right <= 0: # Se a nuvem saiu pela esquerda...
                max_right = max(r.right for r in self.copias)
                rect.x = max_right + random.randint(50, 200) # Adiciona um espaço aleatório
                rect.y = random.randint(30, 200) # Sorteia uma nova altura também

    def draw(self, tela):
        for rect in self.copias:
            tela.blit(self.image, rect)
