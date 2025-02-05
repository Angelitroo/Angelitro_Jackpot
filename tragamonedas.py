import pygame
import random
from icono import Icono
from constantes import REDUCCION_PREMIO, MUSICA_FONDO, MENSAJE_INICIO, APUESTA, SIN_DINERO, NO_GIRAR, GANASTE, PERDISTE, PAGOS

class Tragamonedas:
    def __init__(self, jackpot_inicial, dinero_inicial):
        pygame.mixer.init()
        pygame.mixer.music.load(MUSICA_FONDO)
        pygame.mixer.music.play(-1)  # Play the music in a loop
        self.jackpot_inicial = jackpot_inicial
        self.dinero_inicial = dinero_inicial
        self.iconos = []
        self.__crear_iconos()
        self.reiniciar()

    def reiniciar(self):
        self.mensaje_actual = MENSAJE_INICIO
        self.jackpot_actual = self.jackpot_inicial
        self.dinero_actual = self.dinero_inicial
        self.resultados = ["Siete"] * 3
        self.apuesta_actual = 0

    def __crear_iconos(self):
        self.iconos = [
            Icono("Triste", "sadface.png"),
            Icono("Sombrero", "katipunero_hat.png"),
            Icono("Bandana", "bandana.png"),
            Icono("Camisa", "camesa_de_chino.png"),
            Icono("Banyal", "banyal.png"),
            Icono("Tsinelas", "tsinelas.png"),
            Icono("Arnis", "arnis.png"),
            Icono("Siete", "siete.png")
        ]

    def establecer_apuesta(self, apuesta):
        if self.dinero_actual >= apuesta:
            self.apuesta_actual = apuesta
            self.mensaje_actual = f"{APUESTA} {self.apuesta_actual}"
        else:
            self.mensaje_actual = SIN_DINERO

    def obtener_mensaje_actual(self):
        return self.mensaje_actual

    def girar(self):
        if self.apuesta_actual <= 0:
            self.mensaje_actual = "Debes realizar una apuesta"
            return [], 0
        if self.dinero_actual >= self.apuesta_actual:
            self.dinero_actual -= self.apuesta_actual
            self.resultados = [random.choice(self.iconos).nombre for _ in range(3)]
            cantidad_ganada = self.calcular_ganancia()
            if cantidad_ganada > 0:
                self.dinero_actual += cantidad_ganada  # Sumar la cantidad ganada
                self.mensaje_actual = f"{GANASTE} ${cantidad_ganada}"
            else:
                self.mensaje_actual = PERDISTE
            return self.resultados, cantidad_ganada
        else:
            self.mensaje_actual = NO_GIRAR
            return [], 0

    def calcular_ganancia(self):
        # Ordena los resultados para que coincidan con las claves de la tabla de pagos
        resultados_ordenados = tuple(sorted(self.resultados))
        premio_base = PAGOS.get(resultados_ordenados, 0)
        return int(premio_base * self.apuesta_actual * REDUCCION_PREMIO)

    def obtener_dinero_actual(self):
        return self.dinero_actual

    def animar_giro(self, pantalla, posiciones, botones_apuesta, botones_accion, fondo, duracion=1.0):
        tiempo_inicial = pygame.time.get_ticks()
        while (pygame.time.get_ticks() - tiempo_inicial) / 1000 < duracion:
            pantalla.blit(fondo, (0, 0))  # Dibujar el fondo
            botones_apuesta.draw(pantalla)  # Dibujar los botones de apuesta
            botones_accion.draw(pantalla)  # Dibujar los botones de acción
            for i in range(3):
                icono = random.choice(self.iconos)
                imagen = pygame.image.load(f"assets/images/{icono.imagen_path}")
                pantalla.blit(imagen, posiciones[i])

            # Mostrar la cantidad de dinero en la parte inferior de la pantalla
            dinero_actual = self.obtener_dinero_actual()
            fuente_dinero = pygame.font.Font(None, 74)
            texto_dinero = fuente_dinero.render(f"Dinero: ${dinero_actual}", True, (255, 255, 255))
            pantalla.blit(texto_dinero, (100, 600))

            pygame.display.flip()
            pygame.time.delay(100)  # Pequeña pausa para la animación