import numpy as np
from colorama import Fore, Style, init

# Lista de colores compatibles con colorama
COLORES_VALIDOS = ['RED', 'GREEN', 'YELLOW', 'BLUE', 'MAGENTA', 'CYAN', 'WHITE']

def colorear_texto(texto, color):
    try:
        color_codigo = getattr(Fore, color.upper())
    except AttributeError:
        print("El color especificado no es válido. Se usará el color predeterminado.")
        color_codigo = Fore.WHITE  # Color predeterminado en caso de que el color no sea válido
    return color_codigo + texto + Style.RESET_ALL

def generar_color_aleatorio():
    # Elegir un color aleatorio de la lista de colores válidos
    color_aleatorio = np.random.choice(COLORES_VALIDOS)
    return color_aleatorio

def main():
    # Inicializar colorama (solo necesitas hacerlo una vez)
    init()

    texto = input("Ingresa el texto que deseas colorear: ")

    # Generar un color aleatorio
    color_aleatorio = generar_color_aleatorio()

    texto_coloreado = colorear_texto(texto, color_aleatorio)
    print("Texto coloreado:", texto_coloreado)

if __name__ == "__main__":
    main()