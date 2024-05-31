import turtle

def dibujar_cuadrado(x, y, color):
    turtle.penup()
    turtle.goto(x - 50, y + 50)  # Mover el cursor al punto inicial
    turtle.pendown()
    turtle.fillcolor(color)
    turtle.begin_fill()
    for _ in range(4):
        turtle.forward(100)
        turtle.right(90)
    turtle.end_fill()

def dibujar_linea(x, y, color):
    turtle.pendown()
    turtle.pensize(2)  # Grosor de la línea
    turtle.pencolor(color)
    turtle.goto(x, y)

def dibujar_con_click(x, y):
    color = input("Ingrese el color para dibujar (por ejemplo, 'red', 'blue', 'green', etc.): ")
    dibujar_cuadrado(x, y, color)

def dibujar_con_arrastre(x, y):
    color = input("Ingrese el color para dibujar la línea (por ejemplo, 'red', 'blue', 'green', etc.): ")
    dibujar_linea(x, y, color)

def main():
    turtle.speed(0)  # Establecer la velocidad de dibujo (0 = la más rápida)
    turtle.onscreenclick(dibujar_con_click, 1)  # Llamar a dibujar_con_click con clic izquierdo
    turtle.ondrag(dibujar_con_arrastre, 3)  # Llamar a dibujar_con_arrastre mientras se arrastra con clic derecho
    turtle.mainloop()  # Mantener la ventana abierta

if __name__ == "__main__":
    main()
