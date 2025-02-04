import pygame
import os

class BotonTragamonedas(pygame.sprite.Sprite):
    def __init__(self, nombre_imagen, posicion):
        pygame.sprite.Sprite.__init__(self)
        self.image = self.cargar_imagen(nombre_imagen)
        self.rect = self.image.get_rect()
        self.rect.topleft = posicion
        self.posicion = posicion

    def cargar_imagen(self, nombre_imagen):
        ruta_completa = os.path.join('assets/images', nombre_imagen)
        try:
            imagen = pygame.image.load(ruta_completa).convert_alpha()
            return imagen
        except pygame.error as e:
            print(f"No se pudo cargar la imagen: {nombre_imagen}")
            raise SystemExit(e)

class BotonApuesta(BotonTragamonedas):
    def __init__(self, nombre_imagen, valor_apuesta, posicion):
        super().__init__(nombre_imagen, posicion)
        self.valor_apuesta = valor_apuesta

class BotonAccion(BotonTragamonedas):
    def __init__(self, nombre_imagen, funcion, posicion):
        super().__init__(nombre_imagen, posicion)
        self.funcion = funcion

    def ejecutar(self):
        self.funcion()