import sys
import random
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget, QFileDialog, QDialog, QLabel, QLineEdit, QDialogButtonBox, QFormLayout, QColorDialog
from PyQt5.QtGui import QPixmap, QPainter, QPen, QColor
from PyQt5.QtCore import Qt, QPoint, QTimer

class ImageLoaderApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Dibujar sobre la Imagen")
        self.setGeometry(100, 100, 400, 400)
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
        
        self.color_button = QPushButton("Elegir Color")
        self.color_button.clicked.connect(self.choose_color)
        self.layout.addWidget(self.color_button)

        self.image_path = None
        self.drawing = False
        self.last_point = None
        self.pen_color = QColor("black")
        
        self.points = []
        self.timer = QTimer()
        self.timer.start(1000)  # Actualiza la posición cada segundo
        
        # Definir puntos iniciales
        self.points = [QPoint(50, 50), QPoint(100, 100), QPoint(150, 150)]

        # Iniciar temporizador para mover los puntos
        self.timer = QTimer()
        self.timer.timeout.connect(self.move_points)
        self.timer.start(1000)  # Actualiza la posición cada segundo
        
    def paintEvent(self, event):
        painter = QPainter(self)
        pen = QPen()
        pen.setWidth(5)
        painter.setPen(pen)
        painter.setBrush(QColor("blue"))
        for point in self.points:
            painter.drawEllipse(point, 5, 5)

    def move_points(self):
        for i in range(len(self.points)):
            new_x = self.points[i].x() + random.randint(-5, 5)  # Mueve el punto aleatoriamente en el eje X
            new_y = self.points[i].y() + random.randint(-5, 5)  # Mueve el punto aleatoriamente en el eje Y
            self.points[i] = QPoint(new_x, new_y)
        self.update()
    

    def load_image(self):
        width, height, ok = ImageSizeDialog.get_image_size(self)
        if ok:
            file_path, _ = QFileDialog.getOpenFileName(self, "Seleccionar Imagen", "", "Archivos de Imagen (*.png *.jpg *.jpeg)")
            if file_path:
                self.image_path = file_path
                pixmap = QPixmap(file_path)
                pixmap = pixmap.scaled(width, height, Qt.KeepAspectRatio)
                self.image_label.setPixmap(pixmap)
                self.image_label.mousePressEvent = self.mouse_press_event
                self.image_label.mouseMoveEvent = self.mouse_move_event
                self.image_label.mouseReleaseEvent = self.mouse_release_event
    
                

    def mouse_press_event(self, event):
        if event.buttons() == Qt.LeftButton and self.image_path:
            self.drawing = True
            self.points.append(event.pos())
            self.last_point = event.pos()

    def mouse_move_event(self, event):
        if self.drawing and self.image_path:
            painter = QPainter(self.image_label.pixmap())
            pen = QPen()
            pen.setWidth(3)
            pen.setWidth(3)
            pen.setColor(self.pen_color)
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
                painter = QPainter(self.image_label.pixmap())
                image = self.image_label.pixmap().toImage()
                image.save(file_path)
                for point in self.points:
                    painter.drawPoint(point)               
                
    
    def choose_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.pen_color = color

class ImageSizeDialog(QDialog):
    @staticmethod
    def get_image_size(parent=None):
        dialog = ImageSizeDialog(parent)
        result = dialog.exec_()
        width = dialog.width_input.text()
        height = dialog.height_input.text()
        try:
            width = int(width)
            height = int(height)
        except ValueError:
            return 0, 0, False
        return width, height, result == QDialog.Accepted

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Tamaño de Imagen")
        self.layout = QVBoxLayout()

        form_layout = QFormLayout()
        self.width_input = QLineEdit()
        self.height_input = QLineEdit()
        form_layout.addRow(QLabel("Ancho:"), self.width_input)
        form_layout.addRow(QLabel("Alto:"), self.height_input)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        self.layout.addLayout(form_layout)
        self.layout.addWidget(buttons)

        self.setLayout(self.layout)

def main():
    app = QApplication(sys.argv)
    window = ImageLoaderApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()