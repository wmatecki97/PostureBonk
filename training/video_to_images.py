import cv2
import random
import os
import shutil
from cvzone.SelfiSegmentationModule import SelfiSegmentation

seg = SelfiSegmentation()


def video_to_images(input_video_path, output_image_path):
    global background_images
    video_capture = cv2.VideoCapture(input_video_path)

    if not video_capture.isOpened():
        print("Error: Could not open video file.")
        return

    frame_count = 0

    while True:
        ret, frame = video_capture.read()

        if not ret:
            break

        image_path = f"{output_image_path}/frame_{os.path.basename(input_video_path)+str(frame_count)}.jpg"
        if os.path.isfile(image_path):
            break

        frame = cv2.resize(frame, (160, 90))
        vid_rmbg = seg.removeBG(frame, threshold=0.6)
        cv2.imwrite(image_path, vid_rmbg)

        frame_count += 1

    video_capture.release()


def remove_files_with_copy(folder_path):
    os.makedirs(folder_path, exist_ok=True)
    files = os.listdir(folder_path)

    for file_name in files:
        if '_copy' in file_name:
            file_path = os.path.join(folder_path, file_name)
            os.remove(file_path)


def process_directory(directory, output_directory, files):
    for file in files:
        if file.endswith(".mp4"):
            input_video_path = os.path.join(directory, file)
            video_to_images(input_video_path, output_directory)


def equalize_number_of_samples_for_classes(class_0_output_folder, class_1_output_folder):
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


if __name__ == "__main__":

    correct_video_folder = os.path.join(os.path.dirname(
        os.path.abspath(__file__)), "trainingVideos", "correct")
    print(correct_video_folder)
    invalid_video_folder = os.path.join(os.path.dirname(
        os.path.abspath(__file__)), "trainingVideos", "invalid")

    class_0_output_folder = os.path.join(os.path.dirname(
        os.path.abspath(__file__)), "trainingData", "raw", "class_0")
    class_1_output_folder = os.path.join(os.path.dirname(
        os.path.abspath(__file__)), "trainingData", "raw", "class_1")

    remove_files_with_copy(class_0_output_folder)
    remove_files_with_copy(class_1_output_folder)

    correct_files = os.listdir(correct_video_folder)
    invalid_files = os.listdir(invalid_video_folder)
    process_directory(correct_video_folder,
                      class_0_output_folder, correct_files)
    process_directory(invalid_video_folder,
                      class_1_output_folder, invalid_files)

    equalize_number_of_samples_for_classes(
        class_0_output_folder, class_1_output_folder)
