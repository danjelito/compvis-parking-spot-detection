import cv2
import pickle
import numpy as np
import os
import config
import utils
    
# get video 
cap= cv2.VideoCapture(config.VIDEO_PATH)

# if pos list file already exist, load that
# else, create new pos list
if os.path.exists(config.PATH_SPOT):
    with open(config.PATH_SPOT, 'rb') as f:
        pos_list= pickle.load(f)
else:
    pos_list= None

# loop through each frame of the video
ret= True
frame_num= 1

while ret: 

    # rerun video if finished
    total_frames= cap.get(cv2.CAP_PROP_FRAME_COUNT)
    current_frame= cap.get(cv2.CAP_PROP_POS_FRAMES)
    if current_frame == total_frames:
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

    # read video frame per frame
    ret, frame= cap.read()

    # detect parking spot
    if pos_list:
        frame_processed= utils.process_img(frame)
        num_spots, num_empty, num_nonempty= utils.check_parking_spot(pos_list, 
                                                                     frame_processed,
                                                                     frame,
                                                                     put_text= False)
    # put counter text
    text= f'Empty spots : {num_empty} / {num_spots}'
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 1.5
    font_thickness = 2
    font_color = (255, 255, 255)  
    box_color = (0, 0, 0) 

    # get the size of the text
    (text_width, text_height), _ = cv2.getTextSize(text, font, font_scale, font_thickness)

    # calculate the position to place the text 
    # (bottom-left corner of the text box)
    x = 20
    y = 50

    cv2.rectangle(frame, 
                  (x, y - text_height - 10), 
                  (x + text_width, y + 15), 
                  box_color, -1)
 
    cv2.putText(frame, 
                text, 
                (x, y), 
                font, 
                font_scale, 
                font_color, 
                font_thickness)
    
    # display video
    window_title= 'press q to quit'
    cv2.namedWindow(window_title, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(window_title, (1280, 720))
    cv2.imshow(window_title, frame)

    frame_num += 1

    if cv2.waitKey(15) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
