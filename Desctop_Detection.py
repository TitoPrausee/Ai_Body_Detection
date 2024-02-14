import cv2
import numpy as np
import mss
import mediapipe as mp
import pyautogui
from threading import Thread, Lock
import time

# Initialisiere MediaPipe für die Pose-Erkennung mit den gewünschten Konfigurationen
mp_draw = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.5, min_tracking_confidence=0.5)

class ScreenCapture:
    def __init__(self, monitor_index=1, size=600):
        # Initialisiere mss für Screenshot-Funktionalität und definiere den Erfassungsbereich
        self.sct = mss.mss()
        self.monitor = self.sct.monitors[monitor_index]
        self.size = size
        self.capture_area = {
            "top": self.monitor["top"] + (self.monitor["height"] - size) // 2,
            "left": self.monitor["left"] + (self.monitor["width"] - size) // 2,
            "width": size,
            "height": size,
        }
        self.running = True  # Steuert die Ausführung des Erfassungs-Threads
        self.active = True  # Steuert, ob die Cursorbewegung aktiv ist
        self.img_lock = Lock()  # Synchronisiert den Zugriff auf das zuletzt erfasste Bild
        self.img = None  # Hält das zuletzt erfasste Bild

    def start_capture(self):
        # Hauptmethode für den Erfassungs-Thread
        while self.running:
            if self.active:
                # Erfasse den definierten Bildschirmbereich
                screenshot = self.sct.grab(self.capture_area)
                img = np.array(screenshot)
                img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
                imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                results = pose.process(imgRGB)

                # Wenn Pose-Landmarks erkannt wurden, bewege den Cursor und zeichne die Landmarks
                if results.pose_landmarks:
                    self.move_cursor_based_on_pose(results.pose_landmarks.landmark)
                    mp_draw.draw_landmarks(img, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

                with self.img_lock:
                    self.img = img  # Aktualisiere das zuletzt erfasste Bild

    def move_cursor_based_on_pose(self, landmarks):
        # Bewege den Cursor basierend auf der erkannten Pose
        screen_w, screen_h = pyautogui.size()  # Ermittle die Größe des Bildschirms
        nose = landmarks[mp_pose.PoseLandmark.NOSE.value]

        # Bewege den Cursor nur, wenn die Nase sichtbar ist
        if nose.visibility > 0.5:
            # Berechne und skaliere die Position der Nase auf Bildschirmkoordinaten
            target_x = int((self.capture_area["left"] + nose.x * self.capture_area["width"]) / self.sct.monitors[1]["width"] * screen_w)
            target_y = int((self.capture_area["top"] + nose.y * self.capture_area["height"]) / self.sct.monitors[1]["height"] * screen_h)
            pyautogui.moveTo(target_x, target_y)  # Bewege den Cursor zu dieser Position

def display_capture(capture):
    # Zeige das erfasste Bild und steuere die Anwendung
    cv2.namedWindow('Realtime Capture', cv2.WINDOW_NORMAL)
    while capture.running:
        with capture.img_lock:
            img = capture.img  # Zugriff auf das zuletzt erfasste Bild

        if img is not None:
            cv2.imshow('Realtime Capture', img)  # Zeige das Bild an

        # Behandle Benutzereingaben zur Steuerung der Anwendung
        key = cv2.waitKey(1)
        if key & 0xFF == ord('o'):  # Schalte die Cursorbewegung mit 'o' um
            capture.active = not capture.active
        elif key & 0xFF == ord('q'):  # Beende die Anwendung mit 'q'
            capture.running = False

    capture.stop()  # Räume auf und schließe Fenster

if __name__ == "__main__":
    capture = ScreenCapture()
    thread_capture = Thread(target=capture.start_capture)
    thread_capture.start()  # Starte den Erfassungs-Thread

    display_capture(capture)  # Starte die Anzeige und Steuerung im Hauptthread

    thread_capture.join()  # Warte auf das Ende des Erfassungs-Threads
