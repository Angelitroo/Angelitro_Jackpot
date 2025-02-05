import pygame
from constantes import ANCHO_PANTALLA, ALTO_PANTALLA,FONDO_JUEGO, TITULO_JUEGO, FPS, DINERO_INICIAL
from tragamonedas import Tragamonedas
from botones import BotonApuesta, BotonAccion
from fuente import FuenteDigital


def iniciar_juego():
    pygame.init()
    pantalla = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
    pygame.display.set_caption(TITULO_JUEGO)

    fondo = pygame.image.load(FONDO_JUEGO)
    fondo = pygame.transform.scale(fondo, (ANCHO_PANTALLA, ALTO_PANTALLA))

    tragamonedas = Tragamonedas(10000, DINERO_INICIAL)
    fuente_digital = FuenteDigital(tragamonedas.obtener_mensaje_actual, (100, 140), (0, 0, 0))

    botones_apuesta = pygame.sprite.Group(
BotonApuesta("ten_button.png", 10, (100, 500)),
        BotonApuesta("twenty_button.png", 20, (200, 500)),
        BotonApuesta("fifty_button.png", 50, (300, 500)),
        BotonApuesta("hundred_button.png", 100, (400, 500))
    )

    def manejar_giro():
        if tragamonedas.apuesta_actual <= 0:
            fuente_digital.actualizar_texto("Debes realizar una apuesta")
        elif tragamonedas.obtener_dinero_actual() < tragamonedas.apuesta_actual:
            fuente_digital.actualizar_texto("No tienes suficiente dinero")
        else:
            posiciones = [(60 + i * 200, 250) for i in range(3)]
            tragamonedas.animar_giro(pantalla, posiciones, botones_apuesta, botones_accion, fondo)
            resultados, cantidad_ganada = tragamonedas.girar()
            fuente_digital.actualizar_texto(tragamonedas.obtener_mensaje_actual())

    boton_girar = BotonAccion("spin_button.png", manejar_giro, (470, 500))
    boton_reiniciar = BotonAccion("reset_button.png", tragamonedas.reiniciar, (550, 600))
    boton_salir = BotonAccion("quit_button.png", lambda: pygame.quit(), (550, 700))

    botones_accion = pygame.sprite.Group(boton_girar, boton_reiniciar, boton_salir)

    reloj = pygame.time.Clock()
    jugando = True

    while jugando:
        reloj.tick(FPS)

        if pygame.display.get_surface() is None:
            break

        pantalla.blit(fondo, (0, 0))

        mensaje_apuesta = fuente_digital.actualizar()
        pantalla.blit(mensaje_apuesta, (100, 140))

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                jugando = False
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                for boton in botones_apuesta:
                    if boton.rect.collidepoint(evento.pos):
                        tragamonedas.establecer_apuesta(boton.valor_apuesta)
                        fuente_digital.actualizar_texto(tragamonedas.obtener_mensaje_actual())
                for boton in botones_accion:
                    if boton.rect.collidepoint(evento.pos):
                        boton.ejecutar()

        botones_apuesta.update()
        botones_accion.update()
        botones_apuesta.draw(pantalla)
        botones_accion.draw(pantalla)

        for i, resultado in enumerate(tragamonedas.resultados):
            icono = next(icono for icono in tragamonedas.iconos if icono.nombre == resultado)
            imagen = pygame.image.load(f"assets/images/{icono.imagen_path}")
            pantalla.blit(imagen, (60 + i * 200, 250))

        # Mostrar la cantidad de dinero en la parte inferior de la pantalla
        dinero_actual = tragamonedas.obtener_dinero_actual()
        fuente_dinero = pygame.font.Font(None, 74)
        texto_dinero = fuente_dinero.render(f"Dinero: ${dinero_actual}", True, (255, 255, 255))
        pantalla.blit(texto_dinero, (100, 600))

        pygame.display.flip()

    pygame.quit()