import cv2
import pickle
import numpy as np
import os
import config

# get video 
cap= cv2.VideoCapture(config.VIDEO_PATH)

# if pos list file already exist, load that
# else, create new pos list
if os.path.exists(config.PATH_SPOT):
    with open(config.PATH_SPOT, 'rb') as f:
        pos_list= pickle.load(f)
else:
    pos_list= [(None,None)]

# loop through each frame of the video
ret= True
frame_num= 1

while ret: 

    # read video frame per frame
    ret, frame= cap.read()

    # draw rectangle
    for (x1, y1) in pos_list:
        cv2.rectangle(frame, (x1, y1), (x1 + config.DELTA_X, y1 + config.DELTA_Y), (255, 0, 0), 2)    

    # display video
    window_title= 'press q to quit'
    cv2.namedWindow(window_title, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(window_title, (1280, 720))
    cv2.imshow(window_title, frame)

    frame_num += 1

    if cv2.waitKey(30) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
