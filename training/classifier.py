import tensorflow as tf
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Dense, Flatten
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import os
import cv2
import numpy as np
from tensorflow.keras.callbacks import LearningRateScheduler

def build_image_classifier(input_shape, num_classes):
    model = Sequential()
    model.add(Flatten(input_shape=input_shape))
    model.add(Dense(32, activation='relu'))
    model.add(Dense(num_classes, activation='softmax'))  # Changed to 'softmax' activation

    return model

input_shape = (90,160)
num_classes = 2
learning_rate = 0.0001
batch_size = 8
epochs = 32
steps_per_epoch = 1000

dataset = tf.data.TFRecordDataset('trainingData/data.tfrecords')

model = build_image_classifier(input_shape, num_classes)

optimizer = Adam(learning_rate=learning_rate)
model.compile(optimizer=optimizer, loss='sparse_categorical_crossentropy', metrics=['accuracy'])
# Changed loss to 'sparse_categorical_crossentropy' since labels are integers (0 or 1).
#model = load_model(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..','app','assets', 'image_classifier_model.h5'))

train_datagen = ImageDataGenerator(rescale=1.0 / 255)

def custom_image_generator(generator):
    for x, y in generator:
        x = [modify_image(img) for img in x]
        x = np.array(x)
        yield x, y

def modify_image(img):
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    modified_img = np.where(gray_img < 1, 0, 1)
    return modified_img

# Use the custom generator
train_generator = custom_image_generator(train_datagen.flow_from_directory(
    os.path.join(os.path.dirname(os.path.abspath(__file__))+'/trainingData', 'processed'),
    target_size=(90, 160),
    batch_size=batch_size,
    class_mode='binary',
    classes=['class_0', 'class_1']
))

def lr_schedule(epoch):
    initial_lr = learning_rate
    new_lr = initial_lr * tf.math.exp(-0.5 * epoch)
    return new_lr

lr_scheduler = LearningRateScheduler(lr_schedule)

model.fit(train_generator, epochs=epochs, steps_per_epoch=steps_per_epoch, callbacks=[lr_scheduler])

# Save the model to a file
model.save( os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','app','assets','image_classifier_model.h5'))
