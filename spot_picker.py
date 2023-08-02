import cv2 
import pickle
import os

# list to hold position of each bbox
path_spot= 'output/spot_position.pickle'

# if pos list file already exist, load that
# else, create new pos list
if os.path.exists(path_spot):
    with open(path_spot, 'rb') as f:
        pos_list= pickle.load(f)
else:
    pos_list= []

def mouse_click(events, x, y, flags, params):
    if events == cv2.EVENT_LBUTTONDOWN:
        pos_list.append((x, y))
    elif events == cv2.EVENT_RBUTTONDOWN:
        pos_list.pop(-1)

    # everytime we click, save position to file
    with open(path_spot, 'wb') as f:
        pickle.dump(pos_list, f)

# get image
path_img= 'input/image/carpark.png'
img= cv2.imread(path_img)

# set bbox size
delta_x, delta_y= 105, 39

while True:
    
    window_title= 'press q to quit'
    # display image
    cv2.namedWindow(window_title, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(window_title, (1280, 720))
    cv2.imshow(window_title, img)
    
    # draw rectangle
    for (x1, y1) in pos_list:
        cv2.rectangle(img, (x1, y1), (x1+delta_x, y1+delta_y), (255, 0, 0), 2)

    # create location on left click
    cv2.setMouseCallback(window_title, mouse_click)
    

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break