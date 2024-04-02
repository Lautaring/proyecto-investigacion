import pygame
import pygame_gui

# Inicializar pygame
pygame.init()

# Configuración de la pantalla
screen_width = 523
screen_height = 563
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Dibujar con el mouse")

# Cargar imagen de fondo predeterminada
background = None  # Inicializamos background como None

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Administrador de GUI
manager = pygame_gui.UIManager((screen_width, screen_height))
current_color = RED

# Función para cargar una imagen desde el dispositivo
def load_image_from_device():
    image_path = pygame_gui.windows.UIFileDialog(
        rect=pygame.Rect((0, 0), (400, 200)),
        manager=manager,
        window_title="Seleccionar imagen",
        initial_file_path="./",  # Directorio inicial
        allow_existing_files_only=False
    ).current_file_path
    if image_path:
        return pygame.image.load(image_path).convert()
    else:
        return None

# Función para guardar la imagen dibujada
def save_image():
    pygame.image.save(screen, "dibujo.png")

# Crear botón para cargar imagen
load_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((10, 10), (150, 30)),
                                           text='Cargar Imagen',
                                           manager=manager)

# Crear botón para guardar imagen
save_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((170, 10), (150, 30)),
                                           text='Guardar Imagen',
                                           manager=manager)

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
                if prev_pos and background is not None:  # Verificar si background no es None
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
        elif event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == load_button:
                    background = load_image_from_device()
                elif event.ui_element == save_button:
                    save_image()

        # Procesar eventos de GUI
        manager.process_events(event)

    # Dibujar el fondo
    screen.fill(WHITE)
    if background is not None:  # Verificar si background no es None
        screen.blit(background, (0, 0))

    # Actualizar la pantalla
    manager.update(pygame.time.Clock().tick(60) / 1000.0)
    manager.draw_ui(screen)
    pygame.display.flip()

# Salir de pygame
pygame.quit()
