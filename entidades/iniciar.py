# iniciar.py
import pygame


class Botao:
    """Representa um botão interativo desenhado em uma superfície do pygame."""

    def __init__(self, x, y, texto, fonte, cor_texto='white', 
                 cor_fundo='#4169E1', cor_hover='#6495ED'):
        """Inicializa o botão com texto, estilo e área de clique.

        Args:
            x (int): Coordenada X central do botão.
            y (int): Coordenada Y central do botão.
            texto (str): Texto exibido no botão.
            fonte: Fonte usada para renderizar o texto.
            cor_texto (str, optional): Cor do texto. Padrão é 'white'.
            cor_fundo (str, optional): Cor padrão do botão. Padrão é '#4169E1'.
            cor_hover (str, optional): Cor do botão ao passar o mouse por cima.
        """
        self.fonte = fonte
        self.cor_texto = cor_texto
        self.texto_surf = self.fonte.render(texto, True, self.cor_texto)

        self.cor_fundo = cor_fundo
        self.cor_hover = cor_hover
        self.rect = self.texto_surf.get_rect(center=(x, y)).inflate(20, 20) 
        self.texto_rect = self.texto_surf.get_rect(center=self.rect.center)

        self.clicado = False

    def draw(self, superficie):
        """Desenha o botão na superfície e muda de cor quando o mouse está sobre ele."""
        cor_atual = self.cor_fundo
        pos_mouse = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos_mouse):
            cor_atual = self.cor_hover

        pygame.draw.rect(superficie, cor_atual, self.rect, border_radius=12)
        superficie.blit(self.texto_surf, self.texto_rect)

    def check_click(self):
        """Verifica se o botão foi clicado com o botão esquerdo do mouse.

        Returns:
            bool: True se o botão foi clicado, caso contrário False.
        """
        pos_mouse = pygame.mouse.get_pos()
        acao = False

        if self.rect.collidepoint(pos_mouse):
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicado:
                self.clicado = True
                acao = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicado = False
        return acao
