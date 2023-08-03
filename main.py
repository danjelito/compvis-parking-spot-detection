import cv2
import pickle
import numpy as np
import os
import config


def process_img(img):
    """Process image to dilated binary image."""
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


def draw_rectangle(pos, img, color, thickness):
    """Draw rectangle in image for every spot."""
    if isinstance(pos,list):
        for (x1, y1) in pos:
            x2= x1 + config.DELTA_X
            y2= y1 + config.DELTA_Y
            cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 0), thickness)    
    elif isinstance(pos, tuple):
            x1, y1= pos
            x2= x1 + config.DELTA_X
            y2= y1 + config.DELTA_Y
            cv2.rectangle(img, (x1, y1), (x2, y2), color, thickness) 



def check_parking_spot(pos_list, input_img, output_img, put_text= True,
                       draw_rec= True):
    """Check if a spot is empty or not."""
    num_spots= len(pos_list)
    num_empty= 0
    num_nonempty= num_spots - num_empty

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
        threshold= 650
        if draw_rec:
            color= (0, 255, 0) if count_nonzero <= threshold else (0, 0, 255)
            thickness= 4 if count_nonzero <= threshold else 2
            draw_rectangle((x1, y1), output_img, color, thickness)
        if count_nonzero <= threshold:
            num_empty += 1
    return num_spots, num_empty, num_nonempty

    
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
        num_spots, num_empty, num_nonempty= check_parking_spot(pos_list, 
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

    if cv2.waitKey(30) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
