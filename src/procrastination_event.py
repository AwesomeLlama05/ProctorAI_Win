from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QLineEdit, QMessageBox, QMainWindow
from PyQt5.QtCore import Qt, QTimer
import sys


class ProcrastinationEvent:
    def show_popup(self, ai_message, pledge_message):
        app = QApplication(sys.argv)
        window = FocusPopup(ai_message, pledge_message)
        window.show()
        sys.exit(app.exec_())

    def play_countdown(self, count, brief_message="You have 10 seconds to close it."):
        app = QApplication(sys.argv)
        window = CountdownWindow(count, brief_message)
        window.show()
        sys.exit(app.exec_())


class FocusPopup(QMainWindow):
    def __init__(self, ai_message, pledge_message):
        super().__init__()
        self.setWindowTitle("Focus Reminder")
        self.showFullScreen()
        self.setStyleSheet("background-color: white;")

        layout = QVBoxLayout()

        # AI personalized message at the top with wrapping
        self.ai_message_label = QLabel(ai_message)
        self.ai_message_label.setStyleSheet("font-size: 24px; color: black;")
        self.ai_message_label.setWordWrap(True)
        layout.addWidget(self.ai_message_label, alignment=Qt.AlignTop)

        # Pledge message and entry at the bottom
        self.challenge_text = pledge_message.strip()

        self.label = QLabel("Please type the following to continue working:")
        self.label.setStyleSheet("font-size: 18px; color: black;")
        layout.addWidget(self.label)

        self.challenge_label = QLabel(self.challenge_text)
        self.challenge_label.setStyleSheet("font-size: 16px; color: black;")
        layout.addWidget(self.challenge_label)

        self.entry = QLineEdit()
        self.entry.setStyleSheet("font-size: 16px;")
        self.entry.returnPressed.connect(self.check_input)
        layout.addWidget(self.entry)

        self.result_label = QLabel("")
        self.result_label.setStyleSheet("font-size: 16px; color: black;")
        layout.addWidget(self.result_label)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def check_input(self):
        user_input = self.entry.text()
        if user_input == self.challenge_text:
            self.close()
        else:
            self.result_label.setText("Incorrect input. Please try again.")
            self.result_label.setStyleSheet("color: red;")
            self.entry.clear()


class CountdownWindow(QMainWindow):
    def __init__(self, count, brief_message):
        super().__init__()
        self.setWindowTitle(brief_message)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)

        screen = QApplication.primaryScreen().geometry()
        window_width = 400
        window_height = 100
        position_top = int(screen.height() / 2 - window_height / 2)
        position_right = int(screen.width() / 2 - window_width / 2)
        self.setGeometry(position_right, position_top, window_width, window_height)

        self.label = QLabel("", self)
        self.label.setStyleSheet("font-size: 48px; color: red;")
        self.label.setAlignment(Qt.AlignCenter)
        self.setCentralWidget(self.label)

        self.count = count
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_countdown)
        self.timer.start(1000)
        self.update_countdown()

    def update_countdown(self):
        self.label.setText(str(self.count))
        if self.count > 0:
            self.count -= 1
        else:
            self.timer.stop()
            self.close()


if __name__ == "__main__":
    procrastination_event = ProcrastinationEvent()
    procrastination_event.show_popup("You are procrastinating. Please focus on your work.", "I will focus on my work.")
    procrastination_event.play_countdown(10)
