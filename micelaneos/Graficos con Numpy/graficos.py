import math
import numpy as np
from matplotlib import pyplot as plt


#Datos para el gráfico, pueden ser dos listas en x e y para generar una funcion que queramos
x = np.array(range(20))*0.1
y = np.zeros(len(x))
for i in range(len(x)):
    y[i] = math.sin(x[i])

#Creamos el gráfico
plt.ion()
plt.plot(x, y)

# Dibujar un círculo
def dibujar_circulo(x, y, radio):
    theta = np.linspace(0, 2*np.pi, 100)
    x_circulo = x + radio * np.cos(theta)
    y_circulo = y + radio * np.sin(theta)
    plt.plot(x_circulo, y_circulo, color='blue')

# Dibujar un rectángulo
def dibujar_rectangulo(x, y, ancho, alto):
    x_rectangulo = [x, x + ancho, x + ancho, x, x]
    y_rectangulo = [y, y, y + alto, y + alto, y]
    plt.plot(x_rectangulo, y_rectangulo, color='red')

# Dibujar una línea
def dibujar_linea(x1, y1, x2, y2):
    plt.plot([x1, x2], [y1, y2], color='green')

# Crear la figura
plt.figure()

# Dibujar las figuras
dibujar_circulo(0, 0, 1)
dibujar_rectangulo(-1, -1, 2, 2)
dibujar_linea(-2, 0, 2, 0)

# Configurar el aspecto del gráfico
plt.axis('equal')
plt.grid(True)
plt.xlabel('X')
plt.ylabel('Y')
plt.title('Figuras geométricas')

# Mostrar el gráfico
plt.show()
