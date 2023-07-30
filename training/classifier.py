import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Flatten
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import os

def build_image_classifier(input_shape, num_classes):
    model = Sequential()
    model.add(Flatten(input_shape=input_shape))
    model.add(Dense(128, activation='relu'))
    model.add(Dense(64, activation='relu'))
    model.add(Dense(num_classes, activation='softmax'))  # Changed to 'softmax' activation

    return model

input_shape = (90,160, 3)
num_classes = 2
learning_rate = 0.0001
batch_size = 32
epochs = 5

dataset = tf.data.TFRecordDataset('trainingData/data.tfrecords')

model = build_image_classifier(input_shape, num_classes)

optimizer = Adam(learning_rate=learning_rate)
model.compile(optimizer=optimizer, loss='sparse_categorical_crossentropy', metrics=['accuracy'])
# Changed loss to 'sparse_categorical_crossentropy' since labels are integers (0 or 1).


train_datagen = ImageDataGenerator(rescale=1.0 / 255)
train_generator = train_datagen.flow_from_directory(
    os.path.join(os.path.dirname(os.path.abspath(__file__))+'/trainingData', 'processed'),
    target_size=(90,160),
    batch_size=batch_size,
    class_mode='binary',  # Set class_mode to 'binary' for binary classification.
    classes=['class_0', 'class_1']  # Ensure the correct class folder names are provided.
)

model.fit(train_generator, epochs=epochs)

# Save the model to a file
model.save( os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','app','assets','image_classifier_model.h5'))
