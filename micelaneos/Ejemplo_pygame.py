import pygame
import os

# Inicializar pygame
pygame.init()

# Configurar la pantalla
screen = pygame.display.set_mode((523,563 ))
pygame.display.set_caption("Dibujar con el mouse")

# Cargar imagen de fondo
background = pygame.image.load("calchaqui3.png").convert()

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Coordenadas iniciales del mouse
prev_pos = None

# Color inicial
current_color = RED

# Loop principal
drawing = False
running = True
while running:
    # Manejo de eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Botón izquierdo del mouse
                prev_pos = pygame.mouse.get_pos()
                drawing = True
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  # Botón izquierdo del mouse
                drawing = False
        elif event.type == pygame.MOUSEMOTION:
            if drawing:
                new_pos = pygame.mouse.get_pos()
                if prev_pos:
                    pygame.draw.line(background, current_color, prev_pos, new_pos, 5)
                prev_pos = new_pos
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                current_color = RED
            elif event.key == pygame.K_g:
                current_color = GREEN
            elif event.key == pygame.K_b:
                current_color = BLUE
            elif event.key == pygame.K_k:
                current_color = BLACK
            elif event.key == pygame.K_w:
                current_color = WHITE

    # Dibujar el fondo
    screen.blit(background, (0, 0))

    # Actualizar la pantalla
    pygame.display.flip()

# Salir de pygame
pygame.quit()