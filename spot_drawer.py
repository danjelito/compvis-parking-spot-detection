import cv2 
import pickle
import os
import config

# if pos list file already exist, load that
# else, create new pos list
if os.path.exists(config.PATH_SPOT):
    with open(config.PATH_SPOT, 'rb') as f:
        pos_list= pickle.load(f)
else:
    pos_list= []

def mouse_click(events, x, y, flags, params):
    """Create bbox for one parking spot."""
    if events == cv2.EVENT_LBUTTONDOWN: # append pos with left click
        pos_list.append((x, y))
    elif events == cv2.EVENT_RBUTTONDOWN: # del pos with right click
        for i, (x1, y1) in enumerate(pos_list):
            if x1 < x < x1+config.DELTA_X and y1 < y < y1+config.DELTA_Y :
                pos_list.pop(i)

    # everytime we click, save position to file
    with open(config.PATH_SPOT, 'wb') as f:
        pickle.dump(pos_list, f)

while True:
    
    # get image
    img= cv2.imread(config.PATH_IMG)

    # draw rectangle
    for (x1, y1) in pos_list:
        cv2.rectangle(img, (x1, y1), (x1+config.DELTA_X, y1+config.DELTA_Y), (255, 0, 0), 2)
    
    window_title= 'press q to  quit'
    # display image
    cv2.namedWindow(window_title, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(window_title, (1280, 720))
    cv2.imshow(window_title, img) 

    # create location on left click
    cv2.setMouseCallback(window_title, mouse_click)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break