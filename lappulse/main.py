import sys
from PyQt6.QtWidgets import QApplication

from lappulse.ui.dashboard import DashboardWindow

def main():
    
    app = QApplication(sys.argv)
    
    
    try:
       with open("lappulse/ui/style.qss", "r", encoding="utf-8") as f:
            app.setStyleSheet(f.read())
    except FileNotFoundError:
        print("Style sheet not found, running with default theme.")

    
    window = DashboardWindow()
    window.show()
    
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()