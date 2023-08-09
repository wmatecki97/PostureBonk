## About the project
When the application is running, it will access your computer's camera and analyze your sitting posture in real-time. If it detects incorrect posture, it will block the screen and display the configured alarm message. To resume normal operation, correct your posture to dismiss the alarm.

**The whole camera image processing happens on user machine and is not sent anywhere else**
<div>
  <img src="https://github.com/wmatecki97/PostureBonk/blob/main/examples/tray_application.png?raw=true" alt="Tray application" width="300" height="200">
  <div> Windows tray application </div>
</div>


<div>
  <img src="https://github.com/wmatecki97/PostureBonk/blob/main/examples/correct.jpg?raw=true" alt=" Correct sitting recognition" width="300" height="200">
  <div> Correct sitting recognition </div>
</div>

<table>
  <tr>
    <td valign="top"><img src="https://github.com/wmatecki97/PostureBonk/blob/main/examples/invalid.jpg?raw=true" alt="Incorrect sitting recognition" width="300" height="300"></td>
    <td valign="top"><img src="https://github.com/wmatecki97/PostureBonk/blob/main/examples/blocked_screen.png?raw=true" alt="Blocked screen" width="600" height="300"></td>
  </tr>
    <tr>
    <td valign="top"> Incorrect sitting recognition</td>
    <td valign="top">Blocked screen </td>
  </tr>
</table>


## Compiling the application
the requirements for the application are located in requirements.txt file. Ensure you have everything installed.
To run the app run python app/app.py

## Training
### Steps taken during the training of a neural network to classify correct and incorrect sitting postures using videos of individuals. The training process involves the conversion of videos into images, pre-processing of images, and training the model for accurate classification.

### Step 1: Prepare Training Data

Gather video samples of individuals sitting correctly and incorrectly.
go to "training" directory
Organize the videos by placing correct posture videos in the "trainingVideos/correct" directory and incorrect posture videos in the "trainingVideos/incorrect" directory.
### Step 2: Video to Image Conversion and Background Removal

Execute the "video_to_images.py" script, which will convert each video into a series of images.
The script will also perform background removal to isolate the person from the image background, simplifying the training process.
### Step 3: Image Augmentation for Increased Training Data

To increase the diversity of the training data and improve model generalization, run the "sample_images_multiplier.py" script.
The script will apply random transformations to each input image, such as rotation, scaling, and flipping.
It is essential to shift the person within the image, ensuring they are not always centered in the frame to prevent the model from relying on spatial biases.

### Step 4: Model Training

Begin training the neural network using the preprocessed and augmented data.
Execute the "classifier.py" script, which will train the model to classify correct and incorrect sitting postures based on the provided training data.
The model will learn to distinguish between the two classes and achieve improved accuracy over time.
Uncomment model = load_model... to continue training already pretrained model for your use case

### Note:
Classifier is using black and white images as input because it reduces number of neurons almost 3 times (rgb -> brightness only). 
Additionally the image is not grayscale but only 0/1 to even more simplify the training.


## Generate the Standalone Executable
To create a standalone executable for the application, follow these steps:

Open the command prompt or terminal.
Navigate to the project directory:

cd PostureBonk
python -m PyInstaller --onefile --add-data "app/assets;assets" --add-data "venv/Lib/site-packages/mediapipe/modules;mediapipe/modules" --name "Posture bonk" app/posture_bonk.py
After the process is complete, you will find the standalone executable in the dist directory.

## Troubleshooting
If you encounter any issues or errors while using the application, feel free to create an issue on the GitHub repository. We'll be happy to assist you!

## Contributions
Contributions to this project are welcome! If you have any feature suggestions or bug reports, please open an issue or submit a pull request on the GitHub repository.

## License
This project is licensed under the MIT License. Feel free to use, modify, and distribute the application as per the terms of the license. However, please note that the software comes with no warranties or guarantees of any kind.
