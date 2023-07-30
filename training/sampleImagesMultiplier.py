import os
from keras.preprocessing.image import ImageDataGenerator, save_img
import uuid
import shutil

number_of_copies = 3


def save_image(image, class_name):
    save_directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'trainingData', 'processed', class_name)
    os.makedirs(save_directory, exist_ok=True)

    random_suffix = str(uuid.uuid4())[:8]  # Generate a random 8-character suffix
    new_filename = f"{random_suffix}.jpg"
    image_path = os.path.join(save_directory, new_filename)
    save_img(image_path, image)

def save_images_from_generator(generator):
    nb_of_images_processed = 0
    for x, y in generator:
        nb_of_images_processed += x.shape[0]
        for image_nb in range(x.shape[0]):
            # Get the corresponding class name for the current image batch
            class_name = generator.class_indices
            class_name = [k for k, v in class_name.items() if v == y[image_nb]][0]
            save_image(x[image_nb], class_name)  

if __name__ == '__main__':
    Gen = ImageDataGenerator(
        rotation_range=0,
        width_shift_range=0.1,
        height_shift_range=0.3,
        zoom_range=0.1,
        fill_mode='nearest',
        horizontal_flip=True,
        vertical_flip=False,
        rescale=None,
        preprocessing_function=None
    )


    result_directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'trainingData', 'processed')
    shutil.rmtree(result_directory)
    data_directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'trainingData', 'raw')
    shutil.copytree(data_directory, result_directory)

    for i in range(number_of_copies):
        generator = Gen.flow_from_directory(data_directory, batch_size=10, class_mode='binary', target_size=[90,160])
        save_images_from_generator( generator)
