import whisper
import os
from utils.validator import BaseFile
import torch

class Transcriber(BaseFile):
    def __init__(self, path):
        super().__init__(path)
        self.validate()
        self.devices = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

    def validate(self):
        valid_extensions = [".mp3", ".wav", ".flac", ".aac", ".mp4"]
        self._validate_extension(valid_extensions)

    def transcribe(self):
        model = whisper.load_model("large", device=self.devices)
        result = model.transcribe(self.path)
        with open(os.path.splitext(self.path)[0] + ".txt", "w") as f:
            f.write(result["text"])