import sys
import os
import winreg

def enable_startup():
    key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
    app_name = "LapPulse"

    app_path = os.path.abspath(sys.argv[0])

    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_WRITE)
        winreg.SetValueEx(key, app_name, 0, winreg.REG_SZ, app_path)
        winreg.CloseKey(key)
    except Exception as e:
        print(f"Failed to set startup: {e}")

def disable_startup():
    key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
    app_name = "LapPulse"
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_WRITE)
        winreg.DeleteValue(key, app_name)
        winreg.CloseKey(key)
    except FileNotFoundError:
        pass
    except Exception as e:
        print(f"Failed to disable startup: {e}")
