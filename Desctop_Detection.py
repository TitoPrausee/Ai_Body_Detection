import cv2
import mediapipe as mp
import pyautogui
import numpy as np
import time

mpDraw = mp.solutions.drawing_utils
mpPose = mp.solutions.pose
pose = mpPose.Pose()


capture_fps = 240
capture_interval = 1 / capture_fps


active_mode = True


fps_counter = 0
fps_start_time = time.time()

while True:
    start_time = time.time()


    if active_mode:
        screenshot = pyautogui.screenshot()
        img = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        results = pose.process(imgRGB)
        if results.pose_landmarks:
            mpDraw.draw_landmarks(img, results.pose_landmarks, mpPose.POSE_CONNECTIONS)

  
            head_x = int(results.pose_landmarks.landmark[mpPose.PoseLandmark.NOSE].x * img.shape[1])
            head_y = int(results.pose_landmarks.landmark[mpPose.PoseLandmark.NOSE].y * img.shape[0])
            pyautogui.moveTo(head_x, head_y)

         
            for connection in mpPose.POSE_CONNECTIONS:
                start_point = (int(results.pose_landmarks.landmark[connection[0]].x * img.shape[1]),
                               int(results.pose_landmarks.landmark[connection[0]].y * img.shape[0]))
                end_point = (int(results.pose_landmarks.landmark[connection[1]].x * img.shape[1]),
                             int(results.pose_landmarks.landmark[connection[1]].y * img.shape[0]))

                cv2.line(img, start_point, end_point, (0, 255, 0), 3)


        fps_counter += 1
        if time.time() - fps_start_time >= 1.0:
            fps = fps_counter / (time.time() - fps_start_time)
            cv2.putText(img, f"FPS: {int(fps)}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            fps_counter = 0
            fps_start_time = time.time()

     
        cv2.imshow("Body Parts Overlay", img)


    activity_text = "ACTIVE" if active_mode else "PASSIVE"
    cv2.putText(img, f"Mode: {activity_text}", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)


    key = cv2.waitKey(1)
    if key == 32:  
        active_mode = not active_mode

  
    elapsed_time = time.time() - start_time
    wait_time = max(0, capture_interval - elapsed_time)
    time.sleep(wait_time)


    if key == 27:
        break


cv2.destroyAllWindows()
