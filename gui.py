import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QSystemTrayIcon, QMenu, QStyle, QVBoxLayout, QHBoxLayout, QLabel , QLineEdit, QTextEdit, QPushButton, QWidget, QListWidget, QMessageBox
from PyQt6.QtGui import QAction
from modules.manager import TriggerManager

class KaeGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.tm = TriggerManager()

        self.setWindowTitle("Kae Dashboard")
        self.resize(650, 400)

        self.init_ui()
        self.init_tray()
        self.load_trigger_list()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)

        left_layout = QVBoxLayout()
        left_layout.addWidget(QLabel("Your Active Triggers:"))

        self.list_widget = QListWidget()
        left_layout.addWidget(self.list_widget)

        self.delete_btn = QPushButton("Delete Selected Trigger")
        self.delete_btn .setStyleSheet("background-color: #ffcccc; color: #990000; padding: 6px;")
        self.delete_btn.clicked.connect(self.delete_trigger)
        left_layout.addWidget(self.delete_btn)

        main_layout.addLayout(left_layout, 1)

        right_layout = QVBoxLayout()
        right_layout.addWidget(QLabel("Add New Trigger:"))


        right_layout.addWidget(QLabel("Trigger Word:"))
        self.trigger_input = QLineEdit()
        self.trigger_input.setPlaceholderText("e.g. btw")
        right_layout.addWidget(self.trigger_input)

        right_layout.addWidget(QLabel("Expansion Text:"))
        self.expansion_input = QTextEdit()
        self.expansion_input.setPlaceholderText("e.g. by the way")
        right_layout.addWidget(self.expansion_input)

        self.add_btn = QPushButton("Save Trigger")
        self.add_btn.setStyleSheet("background-color: #d4edda; color: #155724; padding: 6px;")
        self.add_btn.clicked.connect(self.add_trigger)
        right_layout.addWidget(self.add_btn)

        right_layout.addStretch()
        main_layout.addLayout(right_layout, 1)

    def init_tray(self):
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(self.style().standardIcon(
            QStyle.StandardPixmap.SP_ComputerIcon
        ))

        tray_menu = QMenu()

        show_action = QAction("Open Dashboard", self)
        show_action.triggered.connect(self.showNormal)
        tray_menu.addAction(show_action)

        quit_action = QAction("Quit App", self)
        quit_action.triggered.connect(QApplication.quit)
        tray_menu.addAction(quit_action)

        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()

    def load_trigger_list(self):
        self.list_widget.clear()
        self.tm.reload_trigs()
        for trig, expansion in self.tm.triggers.items():
            self.list_widget.addItem(f"{trig} -> {expansion}")

    def add_trigger(self):
        trigger = self.trigger_input.text().strip()
        expansion = self.expansion_input.toPlainText().strip()

        if not trigger or not expansion:
            QMessageBox.warning(self, "Warning", "Both trigger and expansion field must be filled!")
            return

        self.tm.add_trig(trigger, expansion)

        self.trigger_input.clear()
        self.expansion_input.clear()
        self.load_trigger_list()

        QMessageBox.information(self, "success", f"Trigger '{trigger}' added successfully!")

    def delete_trigger(self):
        selected_item = self.list_widget.currentItem()
        if not selected_item:
            QMessageBox.warning(self, "Warning", "Please select a trigger from the list to delete.")

        text = selected_item.text()
        trigger = text.split(" -> ")[0]

        confirm = QMessageBox.question(
            self, "Confirm Deletion",
            f"Are you sure you want to delete '{trigger}?'",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if confirm == QMessageBox.StandardButton.Yes:
            self.tm.remove_trig(trigger)
            self.load_trigger_list()

    def closeEvent(self, event):
        event.ignore()
        self.hide()
        self.tray_icon.showMessage(
            "Kae Dashboard",
            "Dashboard minimized to tray. App is still runnin!",
            QSystemTrayIcon.MessageIcon.Information,
            2000
        )

if __name__ == "__main__":
    app = QApplication(sys.argv)

    app.setQuitOnLastWindowClosed(False)

    window = KaeGUI()
    window.show()
    sys.exit(app.exec())