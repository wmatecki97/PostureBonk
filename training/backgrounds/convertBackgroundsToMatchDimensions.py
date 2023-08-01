import os
import os
from PIL import Image

def convert_images_to_png(input_dir):
    output_dir = os.path.join(input_dir, "converted")
    os.makedirs(output_dir, exist_ok=True)

    for filename in os.listdir(input_dir):
        input_path = os.path.join(input_dir, filename)
        if os.path.isfile(input_path):
            try:
                image = Image.open(input_path)
                image = image.resize((160, 90))

                # Create the output file path with the .png extension
                output_filename = os.path.splitext(filename)[0] + ".jpeg"
                output_path = os.path.join(output_dir, output_filename)

                # Save the converted image as PNG
                image.save(output_path, "JPEG")
                
                # Optionally, you can remove the original image if you want to replace it
                # os.remove(input_path)
            except Exception as e:
                print(f"Error converting {filename}: {e}")


if __name__ == "__main__":
    input_directory = os.path.join(os.path.dirname(os.path.abspath(__file__)),'backgrounds')  # Replace this with your input directory path
    convert_images_to_png(input_directory)
