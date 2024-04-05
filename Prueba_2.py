import turtle

# Lista para almacenar las coordenadas de las líneas
coordenadas_lineas = []

def dibujar_linea(x, y):
    # Agregar las coordenadas a la lista solo si es un nuevo clic
    if len(coordenadas_lineas) == 0 or coordenadas_lineas[-1] != (x, y):
        coordenadas_lineas.append((x, y))
    
    # Limpiar la pantalla
    turtle.clear()
    
    # Dibujar todas las líneas
    for i in range(0, len(coordenadas_lineas), 2):
        turtle.penup()
        turtle.goto(coordenadas_lineas[i])
        turtle.pendown()
        turtle.goto(coordenadas_lineas[i + 1] if i + 1 < len(coordenadas_lineas) else (x, y))

def main():
    turtle.speed(0)  # Establecer la velocidad de dibujo (0 = la más rápida)
    turtle.ondrag(dibujar_linea, btn=3)  # Llamar a dibujar_linea mientras se arrastra con clic derecho
    turtle.mainloop()  # Mantener la ventana abierta
    turtle.ondrag(dibujar_linea, btn=3)  
if __name__ == "__main__":
    main()
