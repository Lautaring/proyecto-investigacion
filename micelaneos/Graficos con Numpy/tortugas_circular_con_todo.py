import sys
import random
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QFileDialog, QColorDialog
from PyQt5.QtGui import QPixmap, QPainter, QPen, QColor
from PyQt5.QtCore import Qt, QPoint, QTimer

class ImageLoaderApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Dibujar sobre la Imagen")
        self.setGeometry(100, 100, 600, 400)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        # Layout para la imagen y los botones de colorear
        self.image_color_layout = QHBoxLayout()
        self.layout.addLayout(self.image_color_layout)

        self.image_label = QLabel()
        self.image_color_layout.addWidget(self.image_label)

        # Layout para los botones de colorear
        self.color_button_layout = QVBoxLayout()
        self.image_color_layout.addLayout(self.color_button_layout)
        # Botón para elegir un color personalizado
        self.custom_color_button = QPushButton("Color Personalizado")
        self.custom_color_button.clicked.connect(self.choose_custom_color)
        self.color_button_layout.addWidget(self.custom_color_button)
        


        # Layout para los botones de cargar y guardar imagen
        self.bottom_button_layout = QHBoxLayout()
        self.layout.addLayout(self.bottom_button_layout)

        self.load_button = QPushButton("Cargar Imagen")
        self.load_button.clicked.connect(self.load_image)
        self.bottom_button_layout.addWidget(self.load_button)

        self.draw_button = QPushButton("Guardar Imagen")
        self.draw_button.clicked.connect(self.save_image)
        self.bottom_button_layout.addWidget(self.draw_button)

        self.image_path = None
        self.drawing = False
        self.last_point = None
        self.current_color = Qt.red

    def load_image(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Seleccionar Imagen", "", "Archivos de Imagen (*.png *.jpg *.jpeg)")
        if file_path:
            self.image_path = file_path
            pixmap = QPixmap(file_path)
            self.image_label.setPixmap(pixmap)
            self.image_label.mousePressEvent = self.mouse_press_event
            self.image_label.mouseMoveEvent = self.mouse_move_event
            self.image_label.mouseReleaseEvent = self.mouse_release_event

            # Dibujar las tortugas sobre la imagen cargada
            self.paint_turtles()

            # Iniciar el temporizador para mover las tortugas
            self.timer = QTimer(self)
            self.timer.timeout.connect(self.move_turtles)
            self.timer.start(100)  # Actualizar cada 100 ms

    def mouse_press_event(self, event):
        if event.buttons() == Qt.LeftButton and self.image_path:
            self.drawing = True
            self.last_point = event.pos()

    def mouse_move_event(self, event):
        if self.drawing and self.image_path:
            painter = QPainter(self.image_label.pixmap())
            pen = QPen()
            pen.setWidth(3)
            pen.setColor(QColor(self.current_color))
            painter.setPen(pen)
            painter.drawLine(self.last_point, event.pos())
            self.last_point = event.pos()
            self.image_label.update()

    def mouse_release_event(self, event):
        if event.button() == Qt.LeftButton and self.image_path:
            self.drawing = False

    def save_image(self):
        if self.image_path:
            file_path, _ = QFileDialog.getSaveFileName(self, "Guardar Imagen", "", "Archivos de Imagen (*.png *.jpg *.jpeg)")
            if file_path:
                image = self.image_label.pixmap().toImage()
                image.save(file_path)

    def paint_turtles(self):
        if self.image_path:
            painter = QPainter(self.image_label.pixmap())
            painter.setPen(QPen(QColor(self.current_color), 3))
            self.turtles = []
            for _ in range(2000):
                x = random.randint(0, self.image_label.width())
                y = random.randint(0, self.image_label.height())
                self.turtles.append((x, y))
                painter.drawEllipse(x, y, 10, 20)
            self.image_label.update()

    def move_turtles(self):
        if self.image_path:
            painter = QPainter(self.image_label.pixmap())
            painter.setPen(QPen(QColor(Qt.white)))
            for x, y in self.turtles:
                painter.drawEllipse(x, y, 10, 20)
            self.turtles = [(x + random.randint(-5, 5), y + random.randint(-5, 5)) for x, y in self.turtles]
            painter.setPen(QPen(QColor(self.current_color), 3))
            for x, y in self.turtles:
                painter.drawEllipse(x, y, 10, 20)
            self.image_label.update()

    def choose_custom_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.set_color(color)

    def set_color(self, color):
        self.current_color = color

def main():
    app = QApplication(sys.argv)
    window = ImageLoaderApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
