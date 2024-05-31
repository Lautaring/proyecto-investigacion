from .Celda import Celda

class Tablero:
    def __init__(self, filas, columnas):
        self.filas = filas
        self.columnas = columnas
        self.celdas = [[None for _ in range(columnas)] for _ in range(filas)]

    def agregar_celda(self, fila, columna, color):
        if 0 <= fila < self.filas and 0 <= columna < self.columnas:
            self.celdas[fila][columna] = Celda(fila, columna, color)
        else:
            print("Error: La posición está fuera de los límites del tablero.")

    def obtener_celda(self, fila, columna):
        if 0 <= fila < self.filas and 0 <= columna < self.columnas:
            return self.celdas[fila][columna]
        else:
            print("Error: La posición está fuera de los límites del tablero.")