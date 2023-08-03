import cv2
from cvzone.SelfiSegmentationModule import SelfiSegmentation
import os
import random

vid = cv2.VideoCapture('F:/Programming/Posture/training/trainingVideos/correct/WIN_20230801_18_24_18_Pro.mp4')
seg = SelfiSegmentation()
backgrounds_directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'backgrounds', 'backgrounds')

def load_backgrounds(backgrounds_directory):
    background_images = []
    for filename in os.listdir(backgrounds_directory):
        if filename.lower().endswith((".jpg", ".jpeg", ".png")):
            background_path = os.path.join(backgrounds_directory, filename)
            background_image = cv2.imread(background_path)
            background_images.append(background_image)
    return background_images

background_images = load_backgrounds(backgrounds_directory)

while True:
    ret, video = vid.read()
    

    if not ret:
        break
   
    cv2.imwrite(, vid_rmbg)
    if cv2.waitKey(1) & 0xFF == 27:
        break