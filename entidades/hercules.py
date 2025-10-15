import pygame
pygame.mixer.init()

som_pulo = pygame.mixer.Sound('sons/pulo.wav')
som_pulo.set_volume(0.4)

class Hercules(pygame.sprite.Sprite):
    def __init__(self, pos) -> None:
        super().__init__()

        self.imagens_run = [pygame.transform.scale(pygame.image.load("Imagens\hercules-correndo1.png").convert_alpha(),(128,128)),pygame.transform.scale(pygame.image.load("Imagens\hercules-correndo2.png").convert_alpha(),(128,128))]
        self.imagem_pulo = pygame.transform.scale(pygame.image.load("Imagens\hercules-pulando.png").convert_alpha(),(128,128))
        self.imagem_abaixa = [pygame.transform.scale(pygame.image.load("Imagens\hercules-abaixa1.png").convert_alpha(),(128,128)),pygame.transform.scale(pygame.image.load("Imagens\hercules-abaixa2.png").convert_alpha(),(128,128))]
        self.imagem_morto = pygame.transform.scale(pygame.image.load("Imagens\hercules-mortinho.png").convert_alpha(),(128,128))
        self.imagem_parado = pygame.transform.scale(pygame.image.load("Imagens\hercules-parado.png").convert_alpha(),(128,128))

        self.imagem = self.imagem_parado

        print(f'altura: {self.imagem.get_height()}, largura {self.imagem.get_width()}')

        self.rect = self.imagem.get_rect(midbottom=pos)

        self.vel_x = 0
        self.vel_y = 0
        self.gravidade = 1
        self.forca_pulo = -18
        self.no_chao = True

        self.anim_index = 0
        self.anim_speed = 0.15
        self.esta_correndo = False
        self.esta_abaixado = False

    def input(self, keys):    
        self.vel_x = 0
        self.esta_correndo = False

        # Andar para os lados
        if keys[pygame.K_LEFT]:
            self.vel_x = -5
            self.esta_correndo = True
        if keys[pygame.K_RIGHT]:
            self.vel_x = 5
            self.esta_correndo = True

        # Pular
        if keys[pygame.K_UP] and self.no_chao:
            self.vel_y = self.forca_pulo
            self.no_chao = False
            som_pulo.play()


        # Abaixar
        if keys[pygame.K_DOWN]:
            self.esta_abaixado = True
        else:
            self.esta_abaixado = False

    def aplicar_gravidade(self):
        self.vel_y += self.gravidade
        self.rect.y += self.vel_y

        # Simular chão
        if self.rect.bottom >= 510:
            self.rect.bottom = 510
            self.vel_y = 0
            self.no_chao = True

    def mover(self):
        self.rect.x += self.vel_x

        # Limites da tela
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > 800:
            self.rect.right = 800

    def animar(self):
        # Escolher imagem conforme o estado
        if not self.no_chao:
            self.image = self.imagem_pulo
        elif self.esta_abaixado:
            self.anim_index += self.anim_speed
            if self.anim_index >= len(self.imagem_abaixa):
                self.anim_index = 0
            self.image = self.imagem_abaixa[int(self.anim_index)]
        elif self.esta_correndo:
            self.anim_index += self.anim_speed
            if self.anim_index >= len(self.imagens_run):
                self.anim_index = 0
            self.image = self.imagens_run[int(self.anim_index)]
        else:
            self.image = self.imagem_parado

    def update(self, keys):
        self.input(keys)
        self.aplicar_gravidade()
        self.mover()
        self.animar()
