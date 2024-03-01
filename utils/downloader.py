from validator import BaseFile
from pytube import YouTube
import os

class Downloader(BaseFile):
    def __init__(self, path):
        super().__init__(path)

        self.filename = ''
        self.file_extension = '.mp4'

    def download_audio(self, default_suffix="_audio_file"):
        yt = YouTube(self.path)
        audio_stream = yt.streams.get_audio_only()
        self.filename = yt.title + default_suffix +self.file_extension
        output_path = os.getcwd()
        audio_stream.download(output_path=output_path, filename=self.filename)
        print(f"Downloaded audio: {self.filename}")