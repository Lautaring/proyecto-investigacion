from .Celda import Celda

class Tablero:
    def __init__(self, canvas, filas, columnas):
        self.filas = filas
        self.columnas = columnas
        self.canvas = canvas
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
    
    def dibujar_tablero(self):
        self.canvas.delete("all")
        for fila in range(self.filas):
            for columna in range(self.columnas):
                celda = self.celdas[fila][columna]
                x1 = columna * self.pixel_size
                y1 = fila * self.pixel_size
                x2 = x1 + self.pixel_size
                y2 = y1 + self.pixel_size
                color = celda.color
                self.canvas.create_rectangle(x1, y1, x2, y2, outline=color, fill=color)