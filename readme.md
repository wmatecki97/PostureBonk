##About the project
When the application is running, it will access your computer's camera and analyze your sitting posture in real-time. If it detects incorrect posture, it will block the screen and display the configured alarm message. To resume normal operation, correct your posture to dismiss the alarm.

##Compiling the application
To run the app run python app/app.py

##Training
TBD

##Generate the Standalone Executable
To create a standalone executable for the application, follow these steps:

Open the command prompt or terminal.
Navigate to the project directory:

cd PostureBonk
python -m PyInstaller --onefile --add-data "app/assets;assets" app/app.py
After the process is complete, you will find the standalone executable in the dist directory.

##Troubleshooting
If you encounter any issues or errors while using the application, feel free to create an issue on the GitHub repository. We'll be happy to assist you!

##Contributions
Contributions to this project are welcome! If you have any feature suggestions or bug reports, please open an issue or submit a pull request on the GitHub repository.

##License
This project is licensed under the MIT License. Feel free to use, modify, and distribute the application as per the terms of the license. However, please note that the software comes with no warranties or guarantees of any kind.