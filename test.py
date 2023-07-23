import tensorflow as tf
import numpy as np
from tensorflow.keras.models import load_model
import cv2

# Load the saved model
model = load_model('image_classifier_model.h5')

# Assuming you have a function to capture frames from the live camera source
def get_live_frame():
    # Read a frame from the camera
    ret, frame = cap.read()

    # Return the frame (make sure to handle the case when the frame is not read correctly)
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

# Initialize the camera
cap = cv2.VideoCapture(0)  # Use 0 for the default camera or specify the camera index accordingly

# Process live frames for classification
while True:
    frame = get_live_frame()

    # Check if the frame is read successfully
    if frame is not None:
        # Preprocess the frame as shown above
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


    # Break the loop if a termination condition is met (e.g., key press, timeout, etc.)
    # For example:
    # if cv2.waitKey(1) & 0xFF == ord('q'):
    #     break

# Release the camera and close any open windows
cap.release()
cv2.destroyAllWindows()
