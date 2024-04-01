import sys
import random
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget
from PyQt5.QtGui import QPainter, QColor, QPen
from PyQt5.QtCore import Qt, QTimer, QPoint

class PointMoverApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Movimiento de Puntos")
        self.setGeometry(100, 100, 400, 400)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.point_label = QLabel()
        self.layout.addWidget(self.point_label)

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

def main():
    app = QApplication(sys.argv)
    window = PointMoverApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
