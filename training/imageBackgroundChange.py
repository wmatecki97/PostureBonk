import os
import random
from rembg import remove
from PIL import Image
import threading

def load_backgrounds(backgrounds_directory):
    background_images = []
    for filename in os.listdir(backgrounds_directory):
        if filename.lower().endswith((".jpg", ".jpeg", ".png")):
            background_path = os.path.join(backgrounds_directory, filename)
            background_image = Image.open(background_path)
            background_images.append(background_image)
    return background_images

def composite_with_random_background(foreground_path, background_images, output_directory):
    foreground = Image.open(foreground_path)
    no_background = remove(foreground)
    background = random.choice(background_images)
    if foreground.size != background.size:
        background = background.resize(foreground.size)
    composite = Image.alpha_composite(background.convert("RGBA"), no_background)

    output_filename = os.path.splitext(os.path.basename(foreground_path))[0] + "_with_new_background.jpg"
    output_path = os.path.join(output_directory, output_filename)
    composite = composite.convert("RGB")
    composite.save(output_path, format="JPEG")

input_directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'trainingData', 'processed', 'class_1')
backgrounds_directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'backgrounds', 'backgrounds')

background_images = load_backgrounds(backgrounds_directory)

def process_directory(input_directory):
    file_paths = []
    for root, _, files in os.walk(input_directory):
        for file in files:
            if file.lower().endswith((".jpg", ".jpeg", ".png"))  and str(file).find('_with_new_background') == -1:
                foreground_path = os.path.join(root, file)
                file_paths.append(foreground_path)

    random.shuffle(file_paths)

    for file in file_paths:
            foreground_path = os.path.join(root, file)
            composite_with_random_background(foreground_path, background_images, input_directory)

timer_thread = threading.Thread(target=process_directory, args=[input_directory])
timer_thread.daemon = True
timer_thread.start()

input_directory2 = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'trainingData', 'processed', 'class_0')

process_directory(input_directory2)