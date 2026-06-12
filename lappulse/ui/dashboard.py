import json
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel, QVBoxLayout,
    QHBoxLayout, QFrame, QProgressBar, QPushButton, QDialog,
    QSpinBox, QComboBox, QCheckBox,
    QSystemTrayIcon, QMenu
)
from PyQt6.QtGui import QIcon, QAction
from PyQt6.QtCore import QTimer, Qt, QEvent
from lappulse.core.hardware import HardwareMonitor

DARK_QSS_PATH = "lappulse/ui/style.qss"
LIGHT_QSS_PATH = "lappulse/ui/style_light.qss"


class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.db_path = "lappulse_data.json"
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Settings")
        self.setFixedSize(320, 280)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # Maintenance interval section
        lbl = QLabel("Set Maintenance Interval:")
        lbl.setObjectName("CardTitle")
        layout.addWidget(lbl)

        input_layout = QHBoxLayout()

        self.unit_combo = QComboBox()
        self.unit_combo.addItems(["Days", "Seconds"])

        self.interval_input = QSpinBox()
        self.interval_input.setRange(1, 3600)

        input_layout.addWidget(self.interval_input)
        input_layout.addWidget(self.unit_combo)
        layout.addLayout(input_layout)

        with open(self.db_path, "r") as f:
            data = json.load(f)

        saved_seconds = data.get("maintenance_interval_seconds", 30)

        if saved_seconds >= 86400:
            self.interval_input.setValue(int(saved_seconds / 86400))
            self.unit_combo.setCurrentText("Days")
        else:
            self.interval_input.setValue(saved_seconds)
            self.unit_combo.setCurrentText("Seconds")

        # Appearance section
        appearance_lbl = QLabel("Appearance:")
        appearance_lbl.setObjectName("CardTitle")
        layout.addWidget(appearance_lbl)

        self.light_mode_check = QCheckBox("Enable Light Mode")
        self.light_mode_check.setChecked(data.get("theme", "dark") == "light")
        layout.addWidget(self.light_mode_check)

        # Buttons
        btn_layout = QHBoxLayout()

        cancel_btn = QPushButton("Cancel")
        cancel_btn.setObjectName("CancelButton")
        cancel_btn.clicked.connect(self.reject)

        save_btn = QPushButton("Save Settings")
        save_btn.clicked.connect(self.save_settings)

        btn_layout.addWidget(cancel_btn)
        btn_layout.addWidget(save_btn)
        layout.addLayout(btn_layout)

    def save_settings(self):
        value = self.interval_input.value()
        unit = self.unit_combo.currentText()

        if unit == "Days":
            final_seconds = value * 24 * 60 * 60
        else:
            final_seconds = value

        theme = "light" if self.light_mode_check.isChecked() else "dark"

        with open(self.db_path, "r") as f:
            data = json.load(f)

        data["maintenance_interval_seconds"] = final_seconds
        data["theme"] = theme

        with open(self.db_path, "w") as f:
            json.dump(data, f)

        qss_path = LIGHT_QSS_PATH if theme == "light" else DARK_QSS_PATH
        try:
            with open(qss_path, "r", encoding="utf-8") as f:
                QApplication.instance().setStyleSheet(f.read())
        except FileNotFoundError:
            pass

        self.accept()



class DashboardWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.monitor = HardwareMonitor()
        self.init_ui()
        self.init_tray()
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_dashboard)
        self.timer.start(1000)

    def init_ui(self):
        self.setWindowTitle("LapPulse v1.0 Pro")
        self.setFixedSize(400, 650)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(25, 25, 25, 25)
        main_layout.setSpacing(18)

        # 1. Top Header
        header_layout = QHBoxLayout()
        title_label = QLabel("⚡ LapPulse Pro")
        title_label.setObjectName("MainTitle")

        settings_btn = QPushButton("⚙️")
        settings_btn.setFixedSize(35, 35)
        settings_btn.setStyleSheet("font-size: 16px; padding: 0px;")
        settings_btn.clicked.connect(self.open_settings)

        header_layout.addWidget(title_label)
        header_layout.addSpacing(10)
        header_layout.addWidget(settings_btn, alignment=Qt.AlignmentFlag.AlignRight)
        main_layout.addLayout(header_layout)

        # 2. Battery Card
        self.battery_card = QFrame()
        self.battery_card.setObjectName("Card")
        bat_layout = QVBoxLayout(self.battery_card)
        bat_layout.setContentsMargins(15, 15, 15, 15)

        bat_title = QLabel("Battery Status")
        bat_title.setObjectName("CardTitle")
        self.bat_value = QLabel("--%")
        self.bat_value.setObjectName("CardValue")

        self.bat_bar = QProgressBar()
        self.bat_bar.setValue(0)

        bat_layout.addWidget(bat_title)
        bat_layout.addWidget(self.bat_value)
        bat_layout.addWidget(self.bat_bar)
        main_layout.addWidget(self.battery_card)

        # 3. Charger Status Card
        self.charger_card = QFrame()
        self.charger_card.setObjectName("Card")
        char_layout = QVBoxLayout(self.charger_card)

        char_title = QLabel("Power Source")
        char_title.setObjectName("CardTitle")
        self.char_value = QLabel("Checking...")
        self.char_value.setObjectName("StatusActive")

        char_layout.addWidget(char_title)
        char_layout.addWidget(self.char_value)
        main_layout.addWidget(self.charger_card)

        # 4. CPU Usage Card
        self.cpu_card = QFrame()
        self.cpu_card.setObjectName("Card")
        cpu_layout = QVBoxLayout(self.cpu_card)

        cpu_title = QLabel("CPU Load")
        cpu_title.setObjectName("CardTitle")
        self.cpu_value = QLabel("--%")
        self.cpu_value.setObjectName("CardValue")

        self.cpu_bar = QProgressBar()
        self.cpu_bar.setValue(0)

        cpu_layout.addWidget(cpu_title)
        cpu_layout.addWidget(self.cpu_value)
        cpu_layout.addWidget(self.cpu_bar)
        main_layout.addWidget(self.cpu_card)

        #5 memory optimization card
        self.ram_card = QFrame()
        self.ram_card.setObjectName("Card")
        ram_layout = QVBoxLayout(self.ram_card)
        ram_layout.setContentsMargins(15, 15, 15, 15)

        ram_title = QLabel("Memory Optimization")
        ram_title.setObjectName("CardTitle")

        self.btn_ram_clean = QPushButton("Clean RAM")
        self.btn_ram_clean.clicked.connect(self.handle_ram_cleanup)

        ram_layout.addWidget(ram_title)
        ram_layout.addWidget(self.btn_ram_clean)
        main_layout.addWidget(self.ram_card)

    def init_tray(self):
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(self.style().standardIcon(self.style().StandardPixmap.SP_ComputerIcon))
        self.tray_icon.setToolTip("LapPulse")

        # Create the Tray Menu
        tray_menu = QMenu()

        # Action: Show App
        show_action = QAction("Show App", self)
        show_action.triggered.connect(self.showNormal)

        # Action: Optimize RAM (New!)
        optimize_action = QAction("Optimize RAM", self)
        optimize_action.triggered.connect(self.handle_ram_cleanup)

        # Action: Exit
        quit_action = QAction("Exit", self)
        quit_action.triggered.connect(QApplication.instance().quit)

        tray_menu.addAction(show_action)
        tray_menu.addSeparator()
        tray_menu.addAction(optimize_action)
        tray_menu.addSeparator()
        tray_menu.addAction(quit_action)

        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()
        self.tray_icon.activated.connect(self.tray_icon_activated)

    def tray_icon_activated(self, reason):
        if reason == QSystemTrayIcon.ActivationReason.Trigger:
            self.showNormal()
            self.activateWindow()

    def closeEvent(self, event):
        self.hide()
        event.ignore()

    def open_settings(self):
        dialog = SettingsDialog(self)
        dialog.exec()

    def handle_ram_cleanup(self):
        self.btn_ram_clean.setEnabled(False)
        self.btn_ram_clean.setText("Optimizing......")

        try:
            freed_mb = self.monitor.clean_system_ram()
            self.btn_ram_clean.setText(f"Success Freed {freed_mb:.1f} MB")
        except Exception as e:
            self.btn_ram_clean.setText("Optimization Failed")
            print(f"Error executing RAM cleanup: {e}")
        finally:
            QTimer.singleShot(2500, lambda: self.btn_ram_clean.setText("Clean RAM"))
            QTimer.singleShot(2500, lambda: self.btn_ram_clean.setEnabled(True))

    def update_dashboard(self):
        metrics = self.monitor.get_system_metrics()

        self.bat_value.setText(f"{metrics['battery_percent']}%")
        self.bat_bar.setValue(int(metrics['battery_percent']))

        self.cpu_value.setText(f"{metrics['cpu_usage']}%")
        self.cpu_bar.setValue(int(metrics['cpu_usage']))

        if metrics['is_plugged']:
            self.char_value.setText("⚡ PLUGGED IN (Direct AC Power)")
            self.char_value.setStyleSheet("color: #34D399;")

            if metrics['trigger_discharge_alert']:
                from plyer import notification
                notification.notify(
    title="🔋 LapPulse Maintenance Alert",
    message="Your laptop has been plugged in for too long! To preserve battery health, please unplug the charger and let it discharge to 20%.",
    app_name="LapPulse",
    timeout=10
)
        else:
            self.char_value.setText("🔋 BATTERY MODE (Discharging)")
            self.char_value.setStyleSheet("color: #FB923C;")
