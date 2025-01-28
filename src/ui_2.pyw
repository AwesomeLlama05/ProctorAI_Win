import sys
import os
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QTextEdit, QPushButton, QVBoxLayout
from PyQt6.QtCore import QPoint
from PyQt6.QtGui import QPainter, QPixmap, QKeySequence, QShortcut

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("position tracker")
        self.setGeometry(100, 100, 300, 250)

        script_dir = os.path.dirname(os.path.abspath(__file__))
        self.texture_path = os.path.join(script_dir, "../assets/space_3.jpg")
        self.texture = QPixmap(self.texture_path)
        if self.texture.isNull():
            print(f"error: couldn't load texture from {self.texture_path}")

        self.position_label = QLabel(self)
        self.position_label.setGeometry(10, 10, 280, 20)
        self.position_label.setStyleSheet("font-size: 14px; color: white;")

        # Add QTextEdit box
        self.plan_input = QTextEdit(self)
        self.plan_input.setGeometry(10, 40, 280, 150)
        self.plan_input.setPlaceholderText("What are your plans today?")

        # Add Submit button
        self.submit_button = QPushButton("Submit (Ctrl+Enter)", self)
        self.submit_button.setGeometry(10, 200, 280, 30)
        self.submit_button.clicked.connect(self.submit_plans)

        # Set layout
        layout = QVBoxLayout()
        layout.addWidget(self.position_label)
        layout.addWidget(self.plan_input)
        layout.addWidget(self.submit_button)
        self.setLayout(layout)

        # shortcut for Ctrl+Enter
        shortcut = QShortcut(QKeySequence("Ctrl+Return"), self)
        shortcut.activated.connect(self.submit_plans)

    def submit_plans(self):
        plans = self.plan_input.toPlainText()
        print(f"Submitted plans: {plans}")

    def paintEvent(self, event):
        super().paintEvent(event)
        if not self.texture.isNull():
            painter = QPainter(self)
            global_pos = self.mapToGlobal(QPoint(0, 0))
            offset_x = global_pos.x() % self.texture.width()
            offset_y = global_pos.y() % self.texture.height()
            painter.drawTiledPixmap(self.rect(), self.texture, QPoint(offset_x, offset_y))

    def moveEvent(self, event):
        super().moveEvent(event)
        self.report_position()
        # repaint to get immediate redraw
        self.repaint()

    def report_position(self):
        pos = self.mapToGlobal(self.rect().topLeft())
        self.position_label.setText(f"widget position on screen: {pos.x()}, {pos.y()}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
