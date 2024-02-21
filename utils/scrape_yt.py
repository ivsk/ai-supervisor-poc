from pytube import YouTube
import os
import subprocess

class AudioProcessor:
    def __init__(self, url, download_path, filename):
        self.url = url
        self.download_path = ''
        self.filename = ''
        self.file_extension = '.mp4'

    def download_audio(self, filename='audio_file'):
        yt = YouTube(self.url)
        audio_stream = yt.streams.get_audio_only()
        self.filename = filename + self.file_extension
        audio_stream.download(output_path=self.download_path, filename=self.filename)
        print(f"Downloaded audio: {self.filename}")

    def convert_mp4_to_wav(self, new_extension='.wav'):
        input_file = os.path.join(self.download_path, self.filename)
        self.filename = os.path.splitext(self.filename)[0] + new_extension
        output_file = os.path.join(self.download_path, self.filename)
        command = ['ffmpeg', '-i', input_file, '-vn', '-acodec', 'pcm_s16le', '-ar', '44100', '-ac', '2', output_file]
        try:
            subprocess.run(command, check=True)
            print(f"Conversion successful: {output_file}")
        except subprocess.CalledProcessError as e:
            print(f"An error occurred during conversion: {e}")

    def remove_first_n_seconds(self, start_time, new_filename_suffix='_trimmed'):
        input_file = os.path.join(self.download_path, self.filename)
        self.filename = os.path.splitext(self.filename)[0] + new_filename_suffix + os.path.splitext(self.filename)[1]
        output_file = os.path.join(self.download_path, self.filename)
        command = ['ffmpeg', '-i', input_file, '-ss', str(start_time), '-acodec', 'copy', output_file]
        try:
            subprocess.run(command, check=True)
            print(f"Successfully removed the first {start_time} seconds: {output_file}")
        except subprocess.CalledProcessError as e:
            print(f"An error occurred: {e}")

    def remove_last_n_seconds(self, end_time, new_filename_suffix='_last_trimmed'):
        input_file = os.path.join(self.download_path, self.filename)
        # Getting the total duration of the audio
        command = ['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of',
                   'default=noprint_wrappers=1:nokey=1', input_file]
        result = subprocess.run(command, stdout=subprocess.PIPE, text=True)
        total_duration = float(result.stdout)

        # Calculate the start time for ffmpeg to stop recording (total duration - end_time)
        start_time = total_duration - end_time

        self.filename = os.path.splitext(self.filename)[0] + new_filename_suffix + os.path.splitext(self.filename)[1]
        output_file = os.path.join(self.download_path, self.filename)
        command = ['ffmpeg', '-i', input_file, '-t', str(start_time), '-acodec', 'copy', output_file]
        try:
            subprocess.run(command, check=True)
            print(f"Successfully removed the last {end_time} seconds: {output_file}")
        except subprocess.CalledProcessError as e:
            print(f"An error occurred: {e}")
