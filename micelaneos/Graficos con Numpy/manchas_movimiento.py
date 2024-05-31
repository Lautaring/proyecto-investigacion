import numpy as np
import matplotlib.pyplot as plt
from shapely.geometry import Polygon
from matplotlib.patches import Polygon as MPPolygon
import time

# Genera coordenadas aleatorias para los contornos de las manchas
def generate_random_polygon(num_vertices=5, scale=10):
    points = np.random.rand(num_vertices, 2) * scale
    return Polygon(points)

# Genera manchas superpuestas
def generate_overlapping_patches(num_patches=5):
    patches = []
    for _ in range(num_patches):
        polygon = generate_random_polygon()
        patches.append(polygon)
    return patches

# Función para dibujar los polígonos en un gráfico
def draw_patches(ax, patches):
    ax.clear()
    ax.set_aspect('equal', 'box')

    for patch in patches:
        mpl_polygon = MPPolygon(np.array(patch.exterior), alpha=0.5, edgecolor='none')
        ax.add_patch(mpl_polygon)

    plt.xlim(0, 10)
    plt.ylim(0, 10)
    plt.gca().set_aspect('equal', adjustable='box')
    plt.draw()
    plt.pause(0.01)

# Genera manchas superpuestas
patches = generate_overlapping_patches(5)

fig, ax = plt.subplots()

for i in range(100):  # Número de pasos de movimiento
    for patch in patches:
        # Movimiento aleatorio de los vértices del polígono
        dx = np.random.uniform(-0.1, 0.1)
        dy = np.random.uniform(-0.1, 0.1)
        new_coords = np.array(patch.exterior.coords) + [dx, dy]
        patch = Polygon(new_coords)

    draw_patches(ax, patches)
    time.sleep(0.1)  # Pausa entre pasos de movimiento

plt.show()
