import numpy as np
import matplotlib.pyplot as plt
from shapely.geometry import Polygon

# Función para generar una forma aleatoria
def generate_random_shape():
    num_points = np.random.randint(3, 10)  # Número aleatorio de puntos para el polígono
    points = np.random.rand(num_points, 2) * 100  # Coordenadas aleatorias entre 0 y 100
    shape = Polygon(points)
    return shape

# Crear una nueva figura
plt.figure()

# Dibujar las manchas
num_manchas = 10
for _ in range(num_manchas):
    shape = generate_random_shape()
    x, y = shape.exterior.xy
    plt.fill(x, y, color='b', alpha=0.5)

# Establecer límites del eje y mostrar la figura
plt.xlim(0, 100)
plt.ylim(0, 100)
plt.gca().set_aspect('equal', adjustable='box')
plt.ion()
plt.plot()
