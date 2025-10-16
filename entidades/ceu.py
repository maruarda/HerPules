import pygame
import random

class Ceu:
    def __init__(self, vel, largura_tela):
        original_nuvem_image = pygame.image.load("Imagens/nuvem.png").convert_alpha()
        self.nuvens_data = []
        num_nuvens = 7
        current_x = 0

        for _ in range(num_nuvens):
            scale_factor = random.uniform(3, 6)
            scaled_width = int(original_nuvem_image.get_width() * scale_factor)
            scaled_height = int(original_nuvem_image.get_height() * scale_factor)
            scaled_image = pygame.transform.scale(original_nuvem_image, (scaled_width, scaled_height))

            alpha_value = max(0, 255 - (scale_factor * 23))
            scaled_image.set_alpha(alpha_value)

            pos_x = current_x
            # <<< 1ª MUDANÇA AQUI
            pos_y = random.randint(0, 90) # Antes era (30, 200)
            rect = scaled_image.get_rect(topleft=(pos_x, pos_y))

            self.nuvens_data.append({'image': scaled_image, 'rect': rect, 'alpha': alpha_value})

            spacing = random.randint(150, 400)
            current_x = rect.right + spacing

        self.vel = vel
        self.largura_tela = largura_tela

    def update(self):
        for nuvem in self.nuvens_data:
            nuvem['rect'].x -= self.vel

        for nuvem in self.nuvens_data:
            if nuvem['rect'].right <= 0:
                max_right = max(n['rect'].right for n in self.nuvens_data)
                spacing = random.randint(150, 400)
                nuvem['rect'].x = max_right + spacing

                scale_factor = random.uniform(3, 6)
                original_nuvem_image = pygame.image.load("Imagens/nuvem.png").convert_alpha()
                scaled_width = int(original_nuvem_image.get_width() * scale_factor)
                scaled_height = int(original_nuvem_image.get_height() * scale_factor)
                nuvem['image'] = pygame.transform.scale(original_nuvem_image, (scaled_width, scaled_height))
                
                alpha_value = max(0, 255 - (scale_factor * 15))
                nuvem['image'].set_alpha(alpha_value)
                
                # <<< 2ª MUDANÇA AQUI
                nuvem['rect'].y = random.randint(0, 90) # Antes era (30, 200)

    def draw(self, tela):
        for nuvem in self.nuvens_data:
            tela.blit(nuvem['image'], nuvem['rect'])