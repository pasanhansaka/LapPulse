import sys
import json
import os
from PyQt6.QtWidgets import QApplication

from lappulse.ui.dashboard import DashboardWindow, DARK_QSS_PATH, LIGHT_QSS_PATH

def main():
    app = QApplication(sys.argv)

    theme = "dark"
    try:
        with open("lappulse_data.json", "r") as f:
            theme = json.load(f).get("theme", "dark")
    except (FileNotFoundError, json.JSONDecodeError):
        pass

    qss_path = LIGHT_QSS_PATH if theme == "light" else DARK_QSS_PATH
    try:
        with open(qss_path, "r", encoding="utf-8") as f:
            app.setStyleSheet(f.read())
    except FileNotFoundError:
        print("Style sheet not found, running with default theme.")

    window = DashboardWindow()
    window.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()