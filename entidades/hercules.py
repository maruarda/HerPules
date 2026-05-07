import pygame
from paths import resource_path


class Hercules(pygame.sprite.Sprite):

    def __init__(self, pos) -> None:
        super().__init__()

        self.image = pygame.image.load(resource_path("Imagens/hercules-parado.png"))
        altura = self.image.get_height() * 3
        largura = self.image.get_width() * 3

        self.imagens_run = [
            pygame.transform.scale(
                pygame.image.load(resource_path("Imagens/hercules-correndo1.png")).convert_alpha(),
                (altura, largura)),
            pygame.transform.scale(
                pygame.image.load(resource_path("Imagens/hercules-correndo2.png")).convert_alpha(),
                (altura, largura))
        ]
        self.imagem_pulo = pygame.transform.scale(
            pygame.image.load(resource_path("Imagens/hercules-pulando.png")).convert_alpha(),
            (altura, largura))
        self.imagem_abaixa = [
            pygame.transform.scale(
                pygame.image.load(resource_path("Imagens/hercules-abaixa1.png")).convert_alpha(), (altura, largura)),
            pygame.transform.scale(
                pygame.image.load(resource_path("Imagens/hercules-abaixa2.png")).convert_alpha(), (altura, largura))
        ]
        self.imagem_morto = pygame.transform.scale(
            pygame.image.load(resource_path("Imagens/hercules-mortinho.png")).convert_alpha(), (altura, largura))
        self.imagem_parado = pygame.transform.scale(
            pygame.image.load(resource_path("Imagens/hercules-parado.png")).convert_alpha(), (altura, largura))

        self.image = pygame.transform.scale(self.image.convert_alpha(), (altura, largura))
        self.rect = self.image.get_rect(midbottom=pos)

        # Física
        self.vel_x = 0
        self.vel_y = 0
        self.gravidade = 1
        self.forca_pulo = -24
        self.no_chao = True

        # Animação
        self.anim_index = 0
        self.anim_speed = 0.15
        self.esta_correndo = False
        self.esta_abaixado = False

    def esta_em_movimento(self):
        return self.esta_correndo or self.esta_abaixado or not self.no_chao

    # def input(self, keys):
        # self.vel_x = 0
        # self.esta_correndo = True

        # Pular
        # if keys[pygame.K_UP] and self.no_chao:
            # self.vel_y = self.forca_pulo
            # self.no_chao = False

        # Abaixar (
        # if keys[pygame.K_DOWN]:
            # self.esta_abaixado = True
        # else:
            # self.esta_abaixado = False

    def aplicar_gravidade(self):
        self.vel_y += self.gravidade
        self.rect.y += self.vel_y

        if self.rect.bottom >= 400:
            self.rect.bottom = 400
            self.vel_y = 0
            self.no_chao = True

    def animar(self):
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
        
        self.mask = pygame.mask.from_surface(self.image)
        old_bottom = self.rect.bottom
        old_centerx = self.rect.centerx
        self.rect = self.image.get_rect()
        self.rect.bottom = old_bottom
        self.rect.centerx = old_centerx

    def pular(self):
        if self.no_chao:
            self.vel_y = self.forca_pulo
            self.no_chao = False

    def abaixar(self, ativo):
        self.esta_abaixado = ativo
        self.esta_correndo = not ativo and self.no_chao

    def update(self):
        if self.no_chao and not self.esta_abaixado:
            self.esta_correndo = True

        self.aplicar_gravidade()
        self.animar()
