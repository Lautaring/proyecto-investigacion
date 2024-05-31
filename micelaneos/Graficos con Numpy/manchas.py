import numpy as np
import matplotlib.pyplot as plt

# Generar datos aleatorios para las manchas
num_manchas = 10
radio_max = 5
x_centros = np.random.uniform(0, 100, num_manchas)
y_centros = np.random.uniform(0, 100, num_manchas)
radios = np.random.uniform(0, radio_max, num_manchas)

# Crear una nueva figura
plt.figure()

# Dibujar las manchas
for i in range(num_manchas):
    circle = plt.Circle((x_centros[i], y_centros[i]), radios[i], color='b', alpha=0.5)
    plt.gca().add_patch(circle)

# Establecer límites del eje y mostrar la figura
plt.xlim(0, 100)
plt.ylim(0, 100)
plt.gca().set_aspect('equal', adjustable='box')
plt.show()
