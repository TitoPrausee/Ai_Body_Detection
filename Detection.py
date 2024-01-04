import cv2
import mediapipe as mp
import tkinter as tk
from PIL import Image, ImageTk

class PoseDetectionApp:
    def __init__(self, root, cap, mp_pose):
        self.root = root
        self.root.title("Pose Detection App")

        self.cap = cap
        self.mp_pose = mp_pose

        self.label = tk.Label(root)
        self.label.pack()

        self.btn_start = tk.Button(root, text="Start Detection", command=self.start_detection)
        self.btn_start.pack()

        self.btn_stop = tk.Button(root, text="Stop Detection", command=self.stop_detection, state=tk.DISABLED)
        self.btn_stop.pack()

        self.is_detecting = False
        self.update()

    def start_detection(self):
        self.is_detecting = True
        self.btn_start.config(state=tk.DISABLED)
        self.btn_stop.config(state=tk.NORMAL)
        self.update()

    def stop_detection(self):
        self.is_detecting = False
        self.btn_start.config(state=tk.NORMAL)
        self.btn_stop.config(state=tk.DISABLED)

    def update(self):
        if self.is_detecting:
            ret, frame = self.cap.read()

            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.mp_pose.process(frame_rgb)

            if results.pose_landmarks:
                mp.solutions.drawing_utils.draw_landmarks(frame, results.pose_landmarks, mp.solutions.pose.POSE_CONNECTIONS)

            img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            img = ImageTk.PhotoImage(img)

            self.label.config(image=img)
            self.label.image = img

            self.root.update()

            self.root.after(10, self.update)  

def main():
    cap = cv2.VideoCapture(0)
    mp_pose = mp.solutions.pose.Pose()

    root = tk.Tk()
    app = PoseDetectionApp(root, cap, mp_pose)
    root.mainloop()

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
