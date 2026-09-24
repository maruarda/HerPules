class InputState:
    """Representa o estado da entrada do jogador para uma iteração do jogo.

    Atributos:
        pular (bool): Indica se o jogador solicitou um pulo.
        abaixar (bool): Indica se o jogador está agachado ou solicitou agachar.
    """

    def __init__(self):
        """Inicializa o estado de entrada com ações vazias por padrão."""
        self.pular = False
        self.abaixar = False
