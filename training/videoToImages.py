import cv2
import random
import os
import shutil
from cvzone.SelfiSegmentationModule import SelfiSegmentation

seg = SelfiSegmentation()
backgrounds_directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'backgrounds', 'backgrounds')

def load_backgrounds(backgrounds_directory):
    background_images = []
    for filename in os.listdir(backgrounds_directory):
        if filename.lower().endswith((".jpg", ".jpeg", ".png")):
            background_path = os.path.join(backgrounds_directory, filename)
            background_image = cv2.imread(background_path)
            if background_image is not None:
                background_image = cv2.resize(background_image, (160, 90))
                background_images.append(background_image)
    return background_images

background_images = load_backgrounds(backgrounds_directory)

def video_to_images(input_video_path, output_image_path):
    global background_images
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
        if os.path.isfile(image_path):
            break;
        
        background = random.choice(background_images)
        frame = cv2.resize(frame,(160,90))
        vid_rmbg = seg.removeBG(frame, background, threshold=0.6)

        cv2.imwrite(image_path, vid_rmbg)
        
        # Increment frame count
        frame_count += 1
    
    # Release the video capture object
    video_capture.release()

def remove_files_with_copy(folder_path):
        # Get the list of all files in the folder
        files = os.listdir(folder_path)

        # Iterate through the files and remove those containing '_copy' in their names
        for file_name in files:
            if '_copy' in file_name:
                file_path = os.path.join(folder_path, file_name)
                os.remove(file_path)

if __name__ == "__main__":

   # Folder paths
    correct_video_folder =os.path.join( os.path.dirname(os.path.abspath(__file__)),"trainingVideos","correct")
    print(correct_video_folder)
    invalid_video_folder =os.path.join(  os.path.dirname(os.path.abspath(__file__)),"trainingVideos","invalid")
    
    # Output folders for the respective classes
    class_0_output_folder = os.path.join( os.path.dirname(os.path.abspath(__file__)),"trainingData", "raw","class_0")
    class_1_output_folder = os.path.join( os.path.dirname(os.path.abspath(__file__)),"trainingData", "raw","class_1")
    
    remove_files_with_copy(class_0_output_folder)
    remove_files_with_copy(class_1_output_folder)

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

    correct_images = os.listdir(class_0_output_folder)
    invalid_images = os.listdir(class_1_output_folder)

    images_to_duplicate = correct_images
    num_to_duplicate = len(invalid_images) - len(correct_images)
    source_folder = class_0_output_folder
    if len(correct_images) > len(invalid_images):
        images_to_duplicate = invalid_images
        num_to_duplicate = len(correct_images) - len(invalid_images)
        source_folder = class_1_output_folder
    
    images_to_duplicate = random.sample(images_to_duplicate, num_to_duplicate)
    for image_name in images_to_duplicate:
        image_path = os.path.join(source_folder, image_name)
        filename_without_extension, extension = os.path.splitext(image_path)
        new_image_name = f"{filename_without_extension}_copy{extension}"
        new_image_path = os.path.join(source_folder, new_image_name)

        shutil.copy(image_path, new_image_path)
    

    
