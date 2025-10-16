import pygame

class Chao(pygame.sprite.Sprite):
    def __init__(self, y_pos, vel):
        super().__init__()

        # Carregar imagem do chão
        self.image = pygame.transform.scale(pygame.image.load("Imagens/chao.png").convert_alpha(),(16*4,16*4))
        self.rect = self.image.get_rect(topleft=(0, y_pos))


        # Cria cópias para loop infinito
        self.copias = []
        quant_copias = 14
        largura_img = self.image.get_width()
        for i in range(quant_copias):
            rect = self.image.get_rect(topleft=(i * largura_img, y_pos))
            self.copias.append(rect)

        # Velocidade do chão
        self.vel = vel

    def update(self):
        for rect in self.copias:
            rect.x -= self.vel

        # Resetar posição quando sair da tela
        largura_img = self.image.get_width()
        for rect in self.copias:
            if rect.right <= 0:
                # Encontrar a cópia mais à direita
                max_right = max(r.right for r in self.copias)
                rect.x = max_right

    def draw(self, tela):
        for rect in self.copias:
            tela.blit(self.image, rect)
