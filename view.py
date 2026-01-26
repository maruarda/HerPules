import pygame

class GameView:
    def __init__(self, largura, altura):
        # Inicializa a tela e fontes
        self.tela = pygame.display.set_mode((largura, altura))
        pygame.display.set_caption("HerPULEs")
        self.largura = largura
        self.altura = altura
        
        # Fontes
        self.fonte_jogo = pygame.font.Font('fontes/8BIT.TTF', 30)
        self.fonte_contagem = pygame.font.Font('fontes/8BIT.TTF', 100)
        self.fonte_gameover = pygame.font.Font('fontes/8BIT.TTF', 80)
        
        # Imagens
        self.fundo = pygame.image.load('Imagens/fundo.jpg').convert()
        self.fundo = pygame.transform.scale(self.fundo, (largura, altura))
        self.fundo.set_alpha(150)
        
        self.imagem_menu = pygame.image.load('Imagens/herpules.png').convert_alpha()
        self.imagem_menu = pygame.transform.scale(self.imagem_menu, (largura//2, altura//2))
        
        self.botao_iniciar = pygame.image.load("Imagens/iniciar.png").convert_alpha()
        self.botao_iniciar = pygame.transform.scale(self.botao_iniciar, (200, 80))
        self.rect_botao_iniciar = self.botao_iniciar.get_rect(center=(largura / 2, altura - 70))

        self.botao_reiniciar = pygame.image.load("Imagens/reiniciar.png").convert_alpha()
        self.botao_reiniciar = pygame.transform.scale(self.botao_reiniciar, (200, 100))
        self.rect_botao_reiniciar = self.botao_reiniciar.get_rect(center=(largura // 2, altura // 2 + 50))
        
        self.retangulo_tela = pygame.Rect(0, 400, largura, altura/3)

    def desenhar(self, model):
        self.tela.blit(self.fundo, (0, 0))
        model.ceu.draw(self.tela)
        
        if model.estado == 'menu':
            rect_menu = self.imagem_menu.get_rect(center=(self.largura / 2, self.altura / 3))
            self.tela.blit(self.imagem_menu, rect_menu)
            self.tela.blit(self.botao_iniciar, self.rect_botao_iniciar)
            
            model.grupo_jogador.draw(self.tela)

        elif model.estado == 'contagem':
            model.grupo_jogador.draw(self.tela)
            model.grupo_obstaculos.draw(self.tela)
            
            texto = self.fonte_contagem.render(str(model.contagem_numero), True, 'black')
            rect = texto.get_rect(center=(self.largura/2, self.altura/3))
            self.tela.blit(texto, rect)

        elif model.estado == 'jogando':
            model.grupo_jogador.draw(self.tela)
            model.grupo_obstaculos.draw(self.tela)
            
            texto_score = self.fonte_jogo.render(f"{model.score:05d}", True, (255, 128, 0))
            self.tela.blit(texto_score, (self.largura - texto_score.get_width() - 20, 20))

        elif model.estado == 'game_over':
            model.hercules.image = model.hercules.imagem_morto
            model.grupo_jogador.draw(self.tela)
            model.grupo_obstaculos.draw(self.tela)
            
            texto_go = self.fonte_gameover.render('GAME OVER', True, (0, 0, 0))
            rect_go = texto_go.get_rect(center=(self.largura//2, self.altura//4))
            self.tela.blit(texto_go, rect_go)
            self.tela.blit(self.botao_reiniciar, self.rect_botao_reiniciar)

        pygame.draw.rect(self.tela, (0, 0, 0), self.retangulo_tela)
        model.chao.draw(self.tela)
        
        pygame.display.flip()