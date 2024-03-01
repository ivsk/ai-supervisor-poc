import os
import subprocess
from utils.validator import BaseFile

class AudioProcessor(BaseFile):
    def __init__(self, path):
        super().__init__(path)
        self.validate()
        self.output_path = self.__split_path()

    def validate(self):
        valid_extensions = [".mp3", ".wav", ".flac", ".aac", ".mp4"]
        self._validate_extension(valid_extensions)

    def __split_path(self):
        split_path = os.path.splitext(self.path)
        return split_path[0] + "_trimmed" + split_path[1]

    def remove_first_n_seconds(self, start_time):
        command = ['ffmpeg', '-i', self.path, '-ss', str(start_time), '-acodec', 'copy', self.output_path]
        try:
            subprocess.run(command, check=True)
            print(f"Successfully removed the first {start_time} seconds: {self.output_path}")
        except subprocess.CalledProcessError as e:
            print(f"An error occurred: {e}")

    def remove_last_n_seconds(self, end_time):

        # Getting the total duration of the audio
        command = ['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of',
                   'default=noprint_wrappers=1:nokey=1', self.path]
        result = subprocess.run(command, stdout=subprocess.PIPE, text=True)
        total_duration = float(result.stdout)

        # Calculate the start time for ffmpeg to stop recording (total duration - end_time)
        start_time = total_duration - end_time
        command = ['ffmpeg', '-i', self.path, '-t', str(start_time), '-acodec', 'copy', self.output_path]
        try:
            subprocess.run(command, check=True)
            print(f"Successfully removed the last {end_time} seconds: {self.output_path}")
        except subprocess.CalledProcessError as e:
            print(f"An error occurred: {e}")
