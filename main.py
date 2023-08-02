import cv2
import numpy as np
import os
from pathlib import Path

# get video 
video_path= 'input/video/parking_1920_1080_loop.mp4'
cap= cv2.VideoCapture(video_path)

# loop through each frame of the video
ret= True
frame_num= 1

while ret: 

    # read video frame per frame
    ret, frame= cap.read()

    # display video
    window_title= 'press q to quit'
    cv2.namedWindow(window_title, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(window_title, (1280, 720))
    cv2.imshow(window_title, frame)

    frame_num += 1

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
