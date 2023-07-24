import cv2
import random
import os

def video_to_images(input_video_path, output_image_path):
    # Open the video file
    video_capture = cv2.VideoCapture(input_video_path)
    
    # Check if the video file was opened successfully
    if not video_capture.isOpened():
        print("Error: Could not open video file.")
        return
    
    # Initialize frame count
    frame_count = 0

    while True:
        # Read a single frame from the video
        ret, frame = video_capture.read()
        
        # If the frame was not read successfully, break out of the loop
        if not ret:
            break
        
        # Save the frame as an image
        image_path = f"{output_image_path}/frame_{os.path.basename(input_video_path)+str(frame_count)}.jpg"
        cv2.imwrite(image_path, frame)
        
        # Increment frame count
        frame_count += 1
    
    # Release the video capture object
    video_capture.release()

if __name__ == "__main__":

   # Folder paths
    correct_video_folder = "F:/Programming/Posture/trainingVideos/correct"
    invalid_video_folder = "F:/Programming/Posture/trainingVideos/invalid"
    
    # Output folders for the respective classes
    class_0_output_folder = "F:/Programming/Posture/trainingData/class_0"
    class_1_output_folder = "F:/Programming/Posture/trainingData/class_1"
    
    # Process the 'correct' video folder
    correct_files = os.listdir(correct_video_folder)
    for file in correct_files:
        if file.endswith(".mp4"):
            input_video_path = os.path.join(correct_video_folder, file)
            video_to_images(input_video_path, class_0_output_folder)
    
    # Process the 'invalid' video folder
    invalid_files = os.listdir(invalid_video_folder)
    for file in invalid_files:
        if file.endswith(".mp4"):
            input_video_path = os.path.join(invalid_video_folder, file)
            video_to_images(input_video_path, class_1_output_folder)
