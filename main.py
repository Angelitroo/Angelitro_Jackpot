from PIL import PngImagePlugin

# Deshabilitar advertencias de libpng
PngImagePlugin.warnings.simplefilter("ignore")

import pygame
from juego import iniciar_juego

def main():
    pygame.init()
    iniciar_juego()

if __name__ == "__main__":
    main()