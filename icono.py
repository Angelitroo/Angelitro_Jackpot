import pygame

class Icono(pygame.sprite.Sprite):
    def __init__(self, nombre, imagen_path):
        super().__init__()
        self.nombre = nombre
        self.imagen_path = imagen_path
        self.imagen = pygame.image.load("assets/images/" + imagen_path).convert_alpha()
        self.rect = self.imagen.get_rect()