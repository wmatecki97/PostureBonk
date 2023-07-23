import cv2

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
        image_path = f"{output_image_path}/frame_{frame_count:04d}.jpg"
        cv2.imwrite(image_path, frame)
        
        # Increment frame count
        frame_count += 1
    
    # Release the video capture object
    video_capture.release()

if __name__ == "__main__":
    input_video_path = "F:/Programming/Posture/trainingVideos/correct.mp4"
    output_image_path = "F:/Programming/Posture/trainingData/0"    # Replace with the folder where you want to save the images

    video_to_images(input_video_path, output_image_path)

    input_video_path = "F:/Programming/Posture/trainingVideos/invalid.mp4"
    output_image_path = "F:/Programming/Posture/trainingData/1"    # Replace with the folder where you want to save the images

    video_to_images(input_video_path, output_image_path)
