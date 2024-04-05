import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QFileDialog, QDialog, QLabel, QLineEdit, QDialogButtonBox, QFormLayout, QSpacerItem, QSizePolicy
from PyQt5.QtGui import QPixmap, QPainter, QPen, QColor
from PyQt5.QtCore import Qt, QPoint
import random
import turtle
import threading

class ImageLoaderApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Dibujar sobre la Imagen")
        self.setGeometry(100, 100, 600, 400)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.image_layout = QHBoxLayout()
        self.layout.addLayout(self.image_layout)

        self.image_label = QLabel()
        self.image_layout.addWidget(self.image_label)

        self.button_layout = QVBoxLayout()
        self.image_layout.addLayout(self.button_layout)

        self.red_button = QPushButton("Rojo")
        self.red_button.clicked.connect(lambda: self.set_color("red"))
        self.button_layout.addWidget(self.red_button)

        self.blue_button = QPushButton("Azul")
        self.blue_button.clicked.connect(lambda: self.set_color("blue"))
        self.button_layout.addWidget(self.blue_button)

        self.green_button = QPushButton("Verde")
        self.green_button.clicked.connect(lambda: self.set_color("green"))
        self.button_layout.addWidget(self.green_button)

        self.image_path = None
        self.drawing = False
        self.last_point = None
        self.current_color = QColor("red")

        self.bottom_buttons_layout = QHBoxLayout()
        self.layout.addLayout(self.bottom_buttons_layout)

        self.load_button = QPushButton("Cargar Imagen")
        self.load_button.clicked.connect(self.load_image)
        self.bottom_buttons_layout.addWidget(self.load_button)

        self.draw_button = QPushButton("Guardar Imagen")
        self.draw_button.clicked.connect(self.save_image)
        self.bottom_buttons_layout.addWidget(self.draw_button)

        self.bottom_buttons_layout.addStretch()

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
            self.last_point = event.pos()

    def mouse_move_event(self, event):
        if self.drawing and self.image_path:
            painter = QPainter(self.image_label.pixmap())
            pen = QPen()
            pen.setWidth(3)
            pen.setColor(self.current_color)
            painter.setPen(pen)
            painter.drawLine(self.last_point, event.pos())
            self.last_point = event.pos()
            self.image_label.update()

    def mouse_release_event(self, event):
        if event.button() == Qt.LeftButton and self.image_path:
            self.drawing = False

    def set_color(self, color_name):
        self.current_color = QColor(color_name)

    def save_image(self):
        if self.image_path:
            file_path, _ = QFileDialog.getSaveFileName(self, "Guardar Imagen", "", "Archivos de Imagen (*.png *.jpg *.jpeg)")
            if file_path:
                image = self.image_label.pixmap().toImage()
                image.save(file_path)

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

def create_person():
    t = turtle.Turtle()
    t.shape("turtle")
    t.color("blue")
    t.penup()
    x = random.randint(-200, 200)
    y = random.randint(-200, 200)
    t.goto(x, y)
    t.pendown()
    t.circle(20)
    t.penup()
    t.goto(x, y)
    t.pendown()
    t.right(90)
    t.forward(50)
    t.left(90)
    t.forward(40)
    t.right(45)
    t.forward(30)
    t.backward(30)
    t.left(90)
    t.forward(30)
    t.backward(30)
    t.right(45)
    t.backward(40)
    t.penup()
    t.goto(x, y)
    t.right(90)
    t.forward(70)
    t.pendown()
    t.right(45)
    t.forward(30)
    t.backward(30)
    t.left(90)
    t.forward(30)
    t.backward(30)
    t.right(45)
    t.backward(40)
    t.penup()
    t.goto(x, y)
    t.right(45)
    t.forward(100)
    t.pendown()
    t.left(135)
    t.forward(60)
    t.backward(60)
    t.left(90)
    t.forward(60)
    t.backward(60)
    t.left(135)
    t.penup()
    t.hideturtle()

def main():
    app = QApplication(sys.argv)
    window = ImageLoaderApp()
    window.show()

    for _ in range(2000):
        threading.Thread(target=create_person).start()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()



