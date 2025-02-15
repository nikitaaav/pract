import sys

from PyQt5.QtCore import Qt, QRectF
from PyQt5.QtGui import QBrush, QPainter
from PyQt5.QtWidgets import QApplication, QMainWindow


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("First")

    def paint(self):
        painter = QPainter(self)
        painter.setRenderHint(QPainter)
        painter.setPen(Qt.NoPen)

        painter.setBrush(QBrush(Qt.white, Qt.SolidPattern))

        painter.drawEllipse(40, 40, 40, 40)


App = QApplication(sys.argv)
window = Window()
sys.exit(App.exec())