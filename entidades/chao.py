import pygame


class Chao(pygame.sprite.Sprite):
    """Representa o chão do cenário, com movimento contínuo em loop."""

    def __init__(self, y_pos, vel):
        """Inicializa o chão e suas cópias para criar o efeito de deslocamento.

        Args:
            y_pos (int): Posição vertical do chão na tela.
            vel (int): Velocidade de deslocamento do chão.
        """
        super().__init__()

        self.image = pygame.transform.scale(
            pygame.image.load("Imagens/chao.png").convert_alpha(),(16*4,16*4))
        self.rect = self.image.get_rect(topleft=(0, y_pos))

        self.copias = []
        quant_copias = 14
        largura_img = self.image.get_width()
        for i in range(quant_copias):
            rect = self.image.get_rect(topleft=(i * largura_img, y_pos))
            self.copias.append(rect)

        self.vel = vel

    def update(self):
        """Move o chão para a esquerda e reinicia as peças ao saírem da tela."""
        for rect in self.copias:
            rect.x -= self.vel

        for rect in self.copias:
            if rect.right <= 0:
                max_right = max(r.right for r in self.copias)
                rect.x = max_right

    def draw(self, tela):
        """Desenha todas as cópias do chão na superfície."""
        for rect in self.copias:
            tela.blit(self.image, rect)
