import subprocess
import sys

def install_dependencies():
    try:
        subprocess.run([sys.executable, '-m', 'pip', 'install', 'mediapipe'])
        subprocess.run([sys.executable, '-m', 'pip', 'install', 'opencv-python'])
        subprocess.run([sys.executable, '-m', 'pip', 'install', 'pyautogui'])
    except Exception as e:
        print(f"Fehler bei der Installation der Abhängigkeiten: {e}")
        sys.exit(1)

if __name__ == "__main__":
    install_dependencies()
    print("Abhängigkeiten erfolgreich installiert.")
