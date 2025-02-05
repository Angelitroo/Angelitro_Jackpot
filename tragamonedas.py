import pygame
import random
from icono import Icono

# Define la tabla de pagos ampliada
PAGOS = {
    ("Siete", "Siete", "Siete"): 1000,
    ("Arnis", "Arnis", "Arnis"): 300,
    ("Tsinelas", "Tsinelas", "Tsinelas"): 200,
    ("Banyal", "Banyal", "Banyal"): 100,
    ("Camisa", "Camisa", "Camisa"): 30,
    ("Bandana", "Bandana", "Bandana"): 20,
    ("Sombrero", "Sombrero", "Sombrero"): 10,
    ("Triste", "Triste", "Triste"): 0,
    ("Siete", "Siete", "Arnis"): 500,
    ("Siete", "Arnis", "Arnis"): 400,
    ("Arnis", "Arnis", "Tsinelas"): 250,
    ("Tsinelas", "Tsinelas", "Banyal"): 150,
    ("Banyal", "Banyal", "Camisa"): 50,
    ("Camisa", "Camisa", "Bandana"): 25,
    ("Bandana", "Bandana", "Sombrero"): 15,
    ("Sombrero", "Sombrero", "Triste"): 5,
    ("Siete", "Siete", "Tsinelas"): 450,
    ("Siete", "Tsinelas", "Tsinelas"): 350,
    ("Arnis", "Arnis", "Banyal"): 200,
    ("Tsinelas", "Tsinelas", "Camisa"): 120,
    ("Banyal", "Banyal", "Bandana"): 60,
    ("Camisa", "Camisa", "Sombrero"): 35,
    ("Bandana", "Bandana", "Triste"): 10,
    ("Sombrero", "Sombrero", "Siete"): 20,
    ("Triste", "Triste", "Siete"): 1,
}

class Tragamonedas:
    MENSAJE_INICIO = "Tragamonedas"
    GANASTE = "Ganaste $"
    PERDISTE = "Perdiste"
    APUESTA = "Apostaste $"
    SIN_DINERO = "No tienes suficiente dinero"
    NO_GIRAR = "No puedes girar"
    APUESTA_INICIAL = 10
    AUMENTO_JACKPOT = 0.15
    REDUCCION_PREMIO = 0.35  # Factor de reducción del premio

    def __init__(self, jackpot_inicial, dinero_inicial):
        pygame.mixer.init()
        self.jackpot_inicial = jackpot_inicial
        self.dinero_inicial = dinero_inicial
        self.iconos = []
        self.__crear_iconos()
        self.reiniciar()

    def reiniciar(self):
        self.mensaje_actual = Tragamonedas.MENSAJE_INICIO
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
            self.mensaje_actual = f"{Tragamonedas.APUESTA} {self.apuesta_actual}"
        else:
            self.mensaje_actual = Tragamonedas.SIN_DINERO

    def obtener_mensaje_actual(self):
        return self.mensaje_actual

    def girar(self):
        if self.apuesta_actual <= 0:
            self.mensaje_actual = "Debes realizar una apuesta"
            return [], 0
        if self.dinero_actual >= self.apuesta_actual:
            self.dinero_actual -= self.apuesta_actual
            self.jackpot_actual += int(self.apuesta_actual * Tragamonedas.AUMENTO_JACKPOT)
            self.resultados = [random.choice(self.iconos).nombre for _ in range(3)]
            cantidad_ganada = self.calcular_ganancia()
            if cantidad_ganada > 0:
                self.dinero_actual += cantidad_ganada  # Sumar la cantidad ganada
                self.mensaje_actual = f"Ganaste ${cantidad_ganada}"
            else:
                self.mensaje_actual = "Perdiste"
            return self.resultados, cantidad_ganada
        else:
            self.mensaje_actual = Tragamonedas.NO_GIRAR
            return [], 0

    def calcular_ganancia(self):
        # Ordena los resultados para que coincidan con las claves de la tabla de pagos
        resultados_ordenados = tuple(sorted(self.resultados))
        premio_base = PAGOS.get(resultados_ordenados, 0)
        return int(premio_base * self.apuesta_actual * Tragamonedas.REDUCCION_PREMIO)

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