# Parking Spot Detection Project

This project uses computer vision techniques to detect and analyze parking spots in a video. It checks whether each parking spot is empty or occupied and provides a count of empty and occupied spots.

## Project Description

The main components of this project are as follows:

1. Video Input: The project takes a video as input, which contains footage of parking spots.

2. Parking Spot Data: If available, the project loads pre-defined parking spot positions from a pickle file. If no data is available, the user can create a new list of parking spot positions.

3. Parking Spot Detection: The project uses computer vision algorithms to detect parking spots in each frame of the video.

4. Parking Spot Analysis: For each frame, the project analyzes the detected parking spots to determine if they are empty or occupied.

5. Video Output: If the output video file does not exist, the project creates a new video file and writes the processed frames with the parking spot analysis results.

## Dependencies

The project requires the following Python libraries:

- OpenCV (`cv2`): For reading and processing video frames.

- NumPy (`np`): For numerical operations and data manipulation.

- Pickle: For saving and loading parking spot data.

## Acknowledgments

This project is inspired by the YouTube channel "Murtaza's Workshop". The video dataset used in this project belongs to Murtaza's Workshop as well.

## Results

The processed video will contain the following information for each frame:

- The total number of parking spots detected.

- The number of empty parking spots.

- The number of occupied parking spots.

- A text overlay indicating the number of empty spots out of the total spots.

## Additional Notes

- The project uses the MJPEG codec (`cv2.VideoWriter_fourcc(*'MJPG')`) to write the output video. Ensure that your system supports this codec.

- The project automatically loops through the video if it reaches the end, allowing continuous analysis.

- To exit the video display, press 'q'.
