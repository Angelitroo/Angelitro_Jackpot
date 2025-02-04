import pygame

class FuenteDigital(pygame.sprite.Sprite):
    def __init__(self, metodo, posicion, color=(196, 65, 46)):
        pygame.sprite.Sprite.__init__(self)
        self.fuente = pygame.font.Font("assets/fonts/DS-DIGIT.TTF", 22)
        self.color_fuente = color
        self.metodo = metodo
        self.posicion = posicion

    def obtener_superficie_renderizada(self):
        return self.fuente.render(str(self.metodo()), True, self.color_fuente)

    def actualizar(self):
        return self.fuente.render(str(self.metodo()), True, self.color_fuente)

    def actualizar_texto(self, texto):
        self.metodo = lambda: texto