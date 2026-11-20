import sys
from PyQt6.QtWidgets import QApplication, QMainWindow

app = QApplication(sys.argv)

window = QMainWindow()
window.setWindowTitle("Kae")
window.resize(800, 600)

window.show()

sys.exit(app.exec())