import tensorflow as tf
import numpy as np
from tensorflow.keras.models import load_model
import cv2
import tkinter as tk
import overlay
import threading

print('loading model')
# Load the saved model
model = load_model('image_classifier_model.h5')
print('model loaded')

def get_live_frame():
    ret, frame = cap.read()

    if ret:
        return frame
    else:
        return None

def preprocess_frame(frame):
    # Resize the frame to match the input shape of the model (90x160 with 3 color channels)
    preprocessed_frame = cv2.resize(frame, (160, 90))

    # Normalize the pixel values to be in the range [0, 1]
    preprocessed_frame = preprocessed_frame.astype('float32') / 255.0

    return preprocessed_frame

print('initializing camera')
# Initialize the camera
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # Use 0 for the default camera or specify the camera index accordingly
print('camera initialized')

while True:
    frame = get_live_frame()

    if frame is not None:
        preprocessed_frame = preprocess_frame(frame)

        # Convert the preprocessed frame to a batch of size 1 (as the model expects a batch)
        batch = np.expand_dims(preprocessed_frame, axis=0)

        # Make predictions using the loaded model
        predictions = model.predict(batch)

        # Assuming binary classification, predictions will be an array with two values
        # where the first value corresponds to class_0 and the second value corresponds to class_1.
        # The class with the highest probability is the predicted class.
        predicted_class = np.argmax(predictions, axis=1)[0]

        # Log the classification result to the console
        if predicted_class == 0:
            print("Class: class_0")
        else:
            print("Class: class_1")
            popup = overlay.create_overlay()
            processing_thread = threading.Thread(target=overlay.run)
            processing_thread.daemon = True  # Set the thread as daemon so it terminates when the main thread ends
            processing_thread.start()


cap.release()
cv2.destroyAllWindows()
