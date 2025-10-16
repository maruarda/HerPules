# iniciar.py

import pygame

class Botao:
    def __init__(self, x, y, texto, fonte, cor_texto='white', cor_fundo='#4169E1', cor_hover='#6495ED'):
        
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
        """Verifica se o botão foi clicado com o botão esquerdo do mouse. Retorna True se foi clicado."""
        pos_mouse = pygame.mouse.get_pos()
        acao = False

        if self.rect.collidepoint(pos_mouse):
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicado:
                self.clicado = True
                acao = True
        
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicado = False
            
        return acao