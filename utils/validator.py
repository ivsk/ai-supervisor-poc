import os
from urllib.parse import urlparse

class BaseFile:
    def __init__(self, path):
        self.path = path
        self.__validate_path()
        if urlparse(self.path).scheme == "":
            self.__validate_file()

    def __validate_path(self):
        # Check if the file_path is a string
        if not isinstance(self.path, str):
            raise ValueError("File path or URL must be a string")

    def __validate_file(self):    # Check if the file exists
        if not os.path.isfile(self.path):
            raise FileNotFoundError("File does not exist")

    def _validate_extension(self, valid_extensions):
        # Check for a valid file extension
        file_extension = os.path.splitext(self.path)[1]
        if file_extension.lower() not in valid_extensions:
            raise ValueError(f"Invalid file format. Allowed formats: {valid_extensions}")
