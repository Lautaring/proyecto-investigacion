import sys
import random
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget, QFileDialog
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

        self.image_label = QLabel()
        self.layout.addWidget(self.image_label)

        self.load_button = QPushButton("Cargar Imagen")
        self.load_button.clicked.connect(self.load_image)
        self.layout.addWidget(self.load_button)

        self.draw_button = QPushButton("Guardar Imagen")
        self.draw_button.clicked.connect(self.save_image)
        self.layout.addWidget(self.draw_button)

        self.image_path = None
        self.drawing = False
        self.last_point = None
        self.current_color = Qt.red

    def load_image(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Seleccionar Imagen", "", "Archivos de Imagen (*.png *.jpg *.jpeg)")
        if file_path:
            self.image_path = file_path
            self.pixmap = QPixmap(file_path)
            self.image_label.setPixmap(self.pixmap)
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
            painter = QPainter(self.pixmap)
            pen = QPen()
            pen.setWidth(3)
            pen.setColor(QColor(self.current_color))
            painter.setPen(pen)
            painter.drawLine(self.last_point, event.pos())
            self.last_point = event.pos()
            self.image_label.setPixmap(self.pixmap)

    def mouse_release_event(self, event):
        if event.button() == Qt.LeftButton and self.image_path:
            self.drawing = False

    def save_image(self):
        if self.image_path:
            file_path, _ = QFileDialog.getSaveFileName(self, "Guardar Imagen", "", "Archivos de Imagen (*.png *.jpg *.jpeg)")
            if file_path:
                image = self.pixmap.toImage()
                image.save(file_path)

    def paint_turtles(self):
        if self.image_path:
            painter = QPainter(self.pixmap)
            self.turtles = []
            for _ in range(2000):
                x = random.randint(0, self.pixmap.width())
                y = random.randint(0, self.pixmap.height())
                self.turtles.append((x, y))
                # Cargar una imagen de persona y dibujarla en lugar de círculos
                person_icon = QPixmap("person_icon.png")  # Ajusta la ruta a tu imagen de persona
                painter.drawPixmap(x, y, person_icon)
            self.image_label.setPixmap(self.pixmap)

    def move_turtles(self):
        if self.image_path:
            painter = QPainter(self.pixmap)
            painter.fillRect(self.pixmap.rect(), Qt.transparent)
            for x, y in self.turtles:
                x = (x + random.randint(-5, 5)) % self.pixmap.width()
                y = (y + random.randint(-5, 5)) % self.pixmap.height()
                person_icon = QPixmap("person_icon.png")
                painter.drawPixmap(x, y, person_icon)
            self.image_label.setPixmap(self.pixmap)

def main():
    app = QApplication(sys.argv)
    window = ImageLoaderApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
