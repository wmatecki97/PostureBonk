import json

class SharedConfig:
    def __init__(self, certainty=0.8, alarm_message="Straighten up!"):
        self.certainty = certainty
        self.alarm_message = alarm_message
        self.file_path = "config.json"
        self.camera = 0
        self.monitor = 0

    def create_from_file():
        instance = SharedConfig()
        try:
            with open(instance.file_path, "r") as file:
                data = json.load(file)
                instance.__dict__.update(data)
        except Exception as e:
            print(f"Error loading the configuration file: {e}")
            instance.save_to_file()
        return instance

    def save_to_file(self, data=None):
        if data is None:
            data = self.__dict__
        try:
            with open(self.file_path, "w") as file:
                json.dump(data, file, indent=4)
            print("Configuration saved successfully.")
        except Exception as e:
            print(f"Error saving the configuration file: {e}")
