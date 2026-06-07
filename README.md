# ⚡ LapPulse Pro

LapPulse is a premium, lightweight hardware monitoring utility designed to extend your laptop's battery lifespan and optimize performance. Built with Python and PyQt6.

## ✨ Features
- **Smart Battery Tracker:** Monitors if the laptop is plugged in at 100% and triggers a maintenance discharge reminder.
- **Live CPU Monitoring:** Provides real-time CPU performance metrics with a modern Fluent progress bar.
- **Premium Dark UI:** Sleek, modern desktop dashboard inspired by Windows 11 design trends.

## 🛠️ Tech Stack
- **Language:** Python 3.12+
- **GUI Framework:** PyQt6
- **Hardware Metrics:** psutil
- **OS Notifications:** plyer

## 🚀 Getting Started

### Prerequisites
Make sure you have Python installed on your system.

### Installation
1. **Clone the repository:**
   ```bash
   git clone [https://github.com/YOUR_USERNAME/LapPulse.git](https://github.com/YOUR_USERNAME/LapPulse.git)
   cd LapPulse

2. **Create and activate a virtual environment:
    ```bash
    python -m venv venv
    # On Windows:
    venv\Scripts\activate

3. **Install dependencies:
    ```bash
    pip install -r requirements.txt


4. **Running the Application
   To launch the dashboard, run the following command from the root directory:

   ```Bash
   python -m lappulse.main
## 🤝 Contributing
We love contributions! LapPulse is an open-source project aimed at helping university students learn how to contribute to real-world software engineering projects.

### How to Contribute:
Fork the repository.

1. **Create a new Feature Branch for your changes:

    ```Bash
    git checkout -b feature/amazing-feature
2. **Commit your changes using descriptive commit messages:

   ```Bash
   git commit -m "feat: add cpu temperature monitoring"
3. **Push your branch to GitHub:

    ```Bash
   git push origin feature/amazing-feature
4. **Open a Pull Request (PR) against the main branch.

💡 Ideas for Future Roadmap (Good First Issues):
Add CPU Temperature (Thermal) tracking.

Create a tray icon so the app runs in the background.

Build a settings window to customize the maintenance reminder interval.

📄 License
This project is open-source and licensed under the MIT License. Feel free to use, modify, and distribute it.

Developed with ❤️ for the student developer community.
