import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QSystemTrayIcon, QMenu, QStyle
from PyQt6.QtGui import QIcon, QAction

class TrayWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Kae Tray")
        self.resize(600, 500)

        self.tray_icon = QSystemTrayIcon(self)

        self.tray_icon.setIcon(self.style().standardIcon(
            QStyle.StandardPixmap.SP_ComputerIcon
        ))

        tray_menu = QMenu()

        show_action = QAction("Open Dashboard", self)
        show_action.triggered.connect(self.show)
        tray_menu.addAction(show_action)

        quit_action = QAction("Quit", self)
        quit_action.triggered.connect(QApplication.quit)
        tray_menu.addAction(quit_action)

        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()

    def closeEvent(self, event):
        event.ignore()
        self.hide()
        self.tray_icon.showMessage(
            "Kae",
            "App is running in the background tray!",
            QSystemTrayIcon.MessageIcon.Information,
            2000
        )

if __name__ == "__main__":
    app = QApplication(sys.argv)

    app.setQuitOnLastWindowClosed(False)

    window = TrayWindow()
    window.show()
    sys.exit(app.exec())