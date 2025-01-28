import sys
import time
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QTextEdit
from PyQt5.QtCore import QProcess

class TestApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.process = None

    def initUI(self):
        self.setWindowTitle('Test QProcess Terminate')
        self.setGeometry(100, 100, 400, 300)

        self.layout = QVBoxLayout()

        self.output_display = QTextEdit(self)
        self.output_display.setReadOnly(True)
        self.layout.addWidget(self.output_display)

        self.start_button = QPushButton('Start Process', self)
        self.start_button.clicked.connect(self.start_process)
        self.layout.addWidget(self.start_button)

        self.terminate_button = QPushButton('Terminate Process', self)
        self.terminate_button.clicked.connect(self.terminate_process)
        self.layout.addWidget(self.terminate_button)

        self.setLayout(self.layout)

    def start_process(self):
        if self.process:
            self.process.terminate()
            self.process.waitForFinished()

        self.process = QProcess(self)
        self.process.setProgram(sys.executable)
        self.process.setArguments(['-c', 'import time; [time.sleep(1) for _ in range(100)]'])
        self.process.setProcessChannelMode(QProcess.MergedChannels)
        self.process.readyReadStandardOutput.connect(self.handle_stdout)
        self.process.start()

        self.output_display.append("Process started.")

    def terminate_process(self):
        if self.process:
            self.process.terminate()
            if not self.process.waitForFinished(3000):  # Wait for 3 seconds
                self.process.kill()  # Forcefully terminate if not finished
            self.output_display.append("Process terminated.")
            self.process = None

    def handle_stdout(self):
        output = self.process.readAllStandardOutput().data().decode()
        self.output_display.append(output)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    test_app = TestApp()
    test_app.show()
    sys.exit(app.exec_())