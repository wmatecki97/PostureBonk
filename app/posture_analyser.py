import numpy as np
from tensorflow.keras.models import load_model
import cv2
import shared_config
import os
from cvzone.SelfiSegmentationModule import SelfiSegmentation

seg = SelfiSegmentation()
cap = None


class PostureAnalyser:
    def __init__(self, shared_config: shared_config.SharedConfig):
        self.config = shared_config
        self.model = load_model(os.path.join(os.path.dirname(
            os.path.abspath(__file__)), 'assets', 'image_classifier_model.h5'))

    def get_live_frame(self, dispose_camera):
        global cap
        if cap is None:
            cap = cv2.VideoCapture(self.config.camera, cv2.CAP_DSHOW)

        ret, frame = cap.read()
        if dispose_camera:
            cap.release()
            cap = None

        if ret:
            return frame
        else:
            return None

    def preprocess_frame(self, frame):
        # Resize the frame to match the input shape of the model (90x160 with 3 color channels)
        preprocessed_frame = cv2.resize(frame, (160, 90))
        preprocessed_frame = seg.removeBG(
            preprocessed_frame, threshold=0.6)
        preprocessed_frame = cv2.cvtColor(
            preprocessed_frame, cv2.COLOR_BGR2GRAY)

        modified_img = np.where(preprocessed_frame < 255, 0, 1)

        return modified_img

    def calculate_if_show_overlay(self, dispose_camera=True):
        frame = self.get_live_frame(dispose_camera)

        if frame is not None:
            preprocessed_frame = self.preprocess_frame(frame)

            if not np.any(preprocessed_frame == 1):  # no person detected
                return (False, preprocessed_frame)

            batch = np.expand_dims(preprocessed_frame, axis=0)

            predictions = self.model.predict(batch)

            print('probability of sitting correctly ' +
                  str(predictions[0][0]*100)+'%')
            chances_sitting_wrong = predictions[0][1]*100
            print('probability of sitting wrong ' +
                  str(chances_sitting_wrong)+'%')

            if predictions[0][1] < self.config.certainty:
                return (False, preprocessed_frame, chances_sitting_wrong)
            else:
                return (True, preprocessed_frame, chances_sitting_wrong)

        return (False, None, 0)
    
    def release():
        if cap is not None:
            cap.release()
