from PIL import Image, ImageTk

class Tablero:
    def __init__(self, canvas, filas, columnas, pixel_size):
        self.filas = filas
        self.columnas = columnas
        self.canvas = canvas
        self.pixel_size = pixel_size
        self.celdas = [[None for _ in range(columnas)] for _ in range(filas)]
    
    def dibujar_tablero(self):
        self.canvas.delete("all")
        for fila in range(self.filas):
            for columna in range(self.columnas):
                celda = self.celdas[fila][columna]
                if celda:
                    x1 = columna * self.pixel_size
                    y1 = fila * self.pixel_size
                    x2 = x1 + self.pixel_size
                    y2 = y1 + self.pixel_size
                    color = celda.color
                    self.canvas.create_rectangle(x1, y1, x2, y2, outline=color, fill=color)

    def cargar_imagen(self, img_path):
        img = Image.open(img_path)
        img = img.convert("RGB") 
        img_width, img_height = img.size

        if img_width != self.columnas * self.pixel_size or img_height != self.filas * self.pixel_size:
            print("Error: Las dimensiones de la imagen no coinciden con el tamaño del tablero.")
            return
        
        for fila in range(self.filas):
            for columna in range(self.columnas):
                x1 = columna * self.pixel_size
                y1 = fila * self.pixel_size
                x2 = x1 + self.pixel_size
                y2 = y1 + self.pixel_size
                color = img.crop((x1, y1, x2, y2)).getpixel((0, 0))
                self.agregar_celda(fila, columna, '#%02x%02x%02x' % color)  # Convertir RGB a hex

        self.dibujar_tablero()

    def guardar_tablero(self, file_path):
        with open(file_path, "w") as file:
            for fila in self.celdas:
                for celda in fila:
                    if celda:
                        file.write(f"{celda.fila},{celda.columna},{celda.color}\n")

    def cargar_tablero(self, file_path):
        self.celdas = [[None for _ in range(self.columnas)] for _ in range(self.filas)]
        with open(file_path, "r") as file:
            for line in file:
                fila, columna, color = line.strip().split(',')
                fila = int(fila)
                columna = int(columna)
                self.agregar_celda(fila, columna, color)
        self.dibujar_tablero()
