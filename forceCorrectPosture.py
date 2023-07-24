import tensorflow as tf
import numpy as np
from tensorflow.keras.models import load_model
import cv2
import tkinter as tk
import overlay
import threading
import time

isDisplayBlocked=False

print('loading model')
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
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW) 
print('camera initialized')

def calculate_if_show_overlay():
    frame = get_live_frame()

    if frame is not None:
        preprocessed_frame = preprocess_frame(frame)

        batch = np.expand_dims(preprocessed_frame, axis=0)

        predictions = model.predict(batch)

        predicted_class = np.argmax(predictions, axis=1)[0]

        if predicted_class == 0:
            print("Class: class_0")
            return False
        else:
            print("Class: class_1")
            return True


overlay.run(calculate_if_show_overlay)

cap.release()
cv2.destroyAllWindows()
