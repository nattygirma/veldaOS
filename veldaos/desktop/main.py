from PyQt6.QtWidgets import QMainWindow, QApplication
from ui.agent_grid import AgentGridWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("VeldaOS Agents")
        self.setCentralWidget(AgentGridWidget())
        self.setMinimumSize(800, 600)

if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec() 