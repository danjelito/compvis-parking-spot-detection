import cv2
import numpy as np
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
            thickness= 5 if count_nonzero <= threshold else 3
            draw_rectangle((x1, y1), output_img, color, thickness)
        if count_nonzero <= threshold:
            num_empty += 1
    return num_spots, num_empty, num_nonempty