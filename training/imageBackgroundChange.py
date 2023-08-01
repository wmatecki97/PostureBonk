import os
import random
from rembg import remove
from PIL import Image

def load_backgrounds(backgrounds_directory):
    background_images = []
    for filename in os.listdir(backgrounds_directory):
        if filename.lower().endswith((".jpg", ".jpeg", ".png")):
            background_path = os.path.join(backgrounds_directory, filename)
            background_image = Image.open(background_path)
            background_images.append(background_image)
    return background_images

def composite_with_random_background(foreground_path, background_images, output_directory):
    # Load the foreground image (with background to be removed)
    foreground = Image.open(foreground_path)

    # Remove the background from the foreground image
    removed_background = remove(foreground)

    # Select a random background image from the cache
    background = random.choice(background_images)

    # Make sure the background image and the removed background have the same size
    if foreground.size != background.size:
        background = background.resize(foreground.size)

    # Composite the foreground image with the new background
    composite = Image.alpha_composite(background.convert("RGBA"), removed_background)

    # Save the final composite image in JPEG format
    output_filename = os.path.splitext(os.path.basename(foreground_path))[0] + "_with_new_background.jpg"
    output_path = os.path.join(output_directory, output_filename)
    composite.save(output_path, format="JPEG")

# Process all images from the given directory recursively
input_directory = "F:\\Programming\\Posture\\training"
backgrounds_directory = "F:\\Programming\\Posture\\backgrounds"
output_directory = "F:\\Programming\\Posture\\training_with_new_backgrounds"

if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# Cache all background images
background_images = load_backgrounds(backgrounds_directory)

for root, _, files in os.walk(input_directory):
    for file in files:
        if file.lower().endswith((".jpg", ".jpeg", ".png")):
            foreground_path = os.path.join(root, file)
            composite_with_random_background(foreground_path, background_images, output_directory)
