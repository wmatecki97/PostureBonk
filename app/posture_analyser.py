import numpy as np
from tensorflow.keras.models import load_model
import cv2
import overlay as overlay
import shared_config
import os 
from cvzone.SelfiSegmentationModule import SelfiSegmentation

seg = SelfiSegmentation()

class PostureAnalyser:
    def __init__(self, shared_config:shared_config.SharedConfig):
        self.config = shared_config

    def run(self):
        model = load_model(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets', 'image_classifier_model.h5'))

        def get_live_frame():
            cap = cv2.VideoCapture(self.config.camera, cv2.CAP_DSHOW) 
            ret, frame = cap.read()
            cap.release()

            if ret:
                return frame
            else:
                return None

        def preprocess_frame(frame):
            # Resize the frame to match the input shape of the model (90x160 with 3 color channels)
            preprocessed_frame = cv2.resize(frame, (160, 90))
            preprocessed_frame = seg.removeBG(preprocessed_frame, threshold=0.6)
            # Normalize the pixel values to be in the range [0, 1]
            preprocessed_frame = preprocessed_frame.astype('float32') / 255.0

            return preprocessed_frame


        def calculate_if_show_overlay():
            frame = get_live_frame()

            if frame is not None:
                preprocessed_frame = preprocess_frame(frame)

                batch = np.expand_dims(preprocessed_frame, axis=0)

                predictions = model.predict(batch)

                print('probability of sitting correctly '+str(predictions[0][0]*100)+'%')
                print('probability of sitting wrong '+str(predictions[0][1]*100)+'%')

                if predictions[0][1] < self.config.certainty:
                    return False
                else:
                    return True
                
        overlay_runner = overlay.ScreenOverlayRunner(self.config, calculate_if_show_overlay)
        overlay_runner.run()

