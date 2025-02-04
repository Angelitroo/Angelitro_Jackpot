import pygame

class Icono(pygame.sprite.Sprite):
  def __init__(self, nombre, multiplicador_total, multiplicador_doble, imagen_path, multiplicador_extra=0):
    super().__init__()
    self.nombre = nombre
    self.imagen_path = imagen_path
    self.imagen = pygame.image.load("assets/images/" + imagen_path).convert_alpha()
    self.rect = self.imagen.get_rect()
    self.multiplicador_total = multiplicador_total
    self.multiplicador_doble = multiplicador_doble
    self.multiplicador_extra = multiplicador_extra