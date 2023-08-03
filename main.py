import cv2
import pickle
import numpy as np
import os
import config


def process_img(img):
    img_gray= cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_blur= cv2.GaussianBlur(img_gray, (3, 3), 1)
    img_bin= cv2.adaptiveThreshold(
        img_blur, 
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
        cv2.THRESH_BINARY_INV, 
        25, 
        16
    )
    img_med= cv2.medianBlur(img_bin, 5)
    img_dilate= cv2.dilate(img_med, np.ones((3, 3), np.uint8), 1)
    return img_dilate


def draw_rectangle(pos, img, color):
    """Draw rectangle in image for every spot."""
    if isinstance(pos,list):
        for (x1, y1) in pos:
            x2= x1 + config.DELTA_X
            y2= y1 + config.DELTA_Y
            cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 0), 2)    
    elif isinstance(pos, tuple):
            x1, y1= pos
            x2= x1 + config.DELTA_X
            y2= y1 + config.DELTA_Y
            cv2.rectangle(img, (x1, y1), (x2, y2), color, 2) 



def check_parking_spot(pos_list, input_img, output_img, put_text= True,
                       draw_rec= True):
    """Check if a spot is empty or not."""
    for (x1, y1) in pos_list:
        x2= x1 + config.DELTA_X
        y2= y1 + config.DELTA_Y
        spot= input_img[y1:y2, x1:x2]
        count_nonzero= cv2.countNonZero(spot)
        if put_text:
            cv2.putText(output_img, 
                        str(count_nonzero), 
                        (x1+25, y1+25),   
                        cv2.FONT_HERSHEY_SIMPLEX, 
                        0.5, 
                        (255, 255, 255), 
                        2
            )
        if draw_rec:
            color= (0, 255, 0) if count_nonzero <= 650 else (0, 0, 255)
            draw_rectangle((x1, y1), output_img, color)

    
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
        frame_processed= process_img(frame)
        check_parking_spot(pos_list, frame_processed, frame)

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
