import cv2
import numpy as np

# Cargar la imagen
img = cv2.imread('Prueba3.png')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
_, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV)

# Encontrar contornos
contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Procesar cada contorno encontrado
for i, contour in enumerate(contours):
    # Crear una máscara en blanco del mismo tamaño que la imagen original
    mask = np.zeros_like(gray)
    cv2.drawContours(mask, [contour], -1, (255), thickness=cv2.FILLED)
    
    # Extraer la figura usando la máscara
    figure = cv2.bitwise_and(img, img, mask=mask)

    # Encontrar el bounding box del contorno
    x, y, w, h = cv2.boundingRect(contour)
    cropped_figure = figure[y:y+h, x:x+w]

    # Guardar la figura como una imagen separada
    cv2.imwrite(f'figure_{i+1}.png', cropped_figure)

    # Mostrar la figura recortada
    cv2.imshow(f'Figura {i+1}', cropped_figure)

# Esperar a que se cierren las ventanas
cv2.waitKey(0)
cv2.destroyAllWindows()

print("Las figuras se han guardado por separado.")
