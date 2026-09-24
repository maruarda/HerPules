import pygame
from entidades.hercules import Hercules
from entidades.obstaculos import Obstaculo
from entidades.ceu import Ceu
from entidades.chao import Chao


class GameModel:
    """Gerencia o estado lógico, física e regras do jogo.

    Essa classe mantém os dados principais do jogo, como pontuação, estado da
    partida, jogador, obstáculos, chão e céu, além de controlar a atualização
    das entidades durante a execução.
    """

    def __init__(self, largura, altura, velocidade_obstaculo=5):
        """Inicializa o modelo do jogo com as dimensões e os elementos centrais.

        Args:
            largura (int): Largura da tela em pixels.
            altura (int): Altura da tela em pixels.
            velocidade_obstaculo (int, optional): Velocidade base usada para
                movimentação dos obstáculos. Padrão é 5.
        """
        self.largura = largura
        self.altura = altura
        self.velocidade_obstaculo = velocidade_obstaculo
        self.score = 0
        self.estado = 'menu'  # menu, calibracao ,contagem, jogando, game_over
        self.contagem_numero = 3

        self.grupo_jogador = pygame.sprite.GroupSingle()
        self.hercules = Hercules(pos=(70, 400))
        self.grupo_jogador.add(self.hercules)

        self.grupo_obstaculos = pygame.sprite.Group()
        self.chao = Chao(y_pos=400, vel=3)
        self.ceu = Ceu(vel=1, largura_tela=largura)

    def iniciar_jogo(self):
        """Prepara a partida para começar a contagem inicial do jogo."""
        self.estado = 'contagem'
        self.contagem_numero = 3

    def iniciar_calibracao(self):
        """Coloca o jogo no estado de calibração antes de iniciar a partida."""
        self.estado = 'calibracao'

    def resetar_jogo(self):
        """Reinicia o estado do jogo para o início da tela inicial.

        Reseta a pontuação, os obstáculos, a posição e animação do herói e
        retorna o jogo ao menu principal.
        """
        self.score = 0
        self.grupo_obstaculos.empty()
        self.hercules.rect.midbottom = (70, 400)
        self.hercules.vel_y = 0
        self.hercules.no_chao = True
        self.hercules.image = self.hercules.imagem_parado
        self.hercules.esta_abaixado = False
        self.hercules.esta_correndo = False
        self.hercules.anim_index = 0
        self.estado = 'menu'
        self.contagem_numero = 3

    def adicionar_obstaculo(self):
        """Cria um novo obstáculo quando a distância mínima for respeitada.

        Evita que obstáculos sejam gerados muito próximos uns dos outros,
        mantendo o cenário mais consistente e jogável.
        """
        distancia_minima = 300

        if len(self.grupo_obstaculos) > 0:
            ultimo = max(self.grupo_obstaculos, key=lambda obs: obs.rect.x)

            if ultimo.rect.x > self.largura - distancia_minima:
                return

        obs = Obstaculo(vel=5, largura_tela=self.largura, altura_chao=400)
        self.grupo_obstaculos.add(obs)

    def update(self, input_state):
        """Atualiza a lógica do jogo conforme o estado atual e a entrada do usuário.

        Args:
            input_state: Objeto contendo as entradas do jogador, como pulo,
                agachar e demais flags relevantes.

        Returns:
            str | None: Retorna "colisao" quando ocorre uma colisão; caso
                contrário, retorna None.
        """
        if self.estado == "jogando":
            if input_state.pular:
                self.hercules.pular()

            self.hercules.abaixar(input_state.abaixar)

            self.grupo_jogador.update()
            self.grupo_obstaculos.update()

            for obstaculo in self.grupo_obstaculos:
                if not obstaculo.ja_pontuou and obstaculo.rect.right < self.hercules.rect.left:
                    self.score += 1
                    obstaculo.ja_pontuou = True

            if self.hercules.esta_em_movimento():
                self.ceu.update()
                self.chao.update()

            if pygame.sprite.spritecollide(
                self.hercules,
                self.grupo_obstaculos,
                False,
                pygame.sprite.collide_mask
            ):
                return "colisao"

        elif self.estado in ["menu", "calibracao", "contagem"]:
            self.grupo_jogador.update()

            if self.hercules.esta_em_movimento():
                self.ceu.update()
                self.chao.update()

        elif self.estado == "game_over":
            # não atualiza nada para tudo ficar parado
            pass

        return None
