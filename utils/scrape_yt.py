from pytube import YouTube
import os
import subprocess

yt = YouTube("https://youtu.be/oWMNskk8nzY?si=plumQqVv8kA0PSgv")

audio_stream = yt.streams.get_audio_only()
audio_stream.download(output_path='', filename='first_test.mp4')

def remove_first_n_seconds(input_file, output_file, start_time):
    command = ['ffmpeg', '-i', input_file, '-ss', str(start_time), '-acodec', 'copy', output_file]
    try:
        subprocess.run(command, check=True)
        print(f"Successfully removed the first {start_time} seconds: {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")


def convert_mp4_to_wav(input_file, output_file):
    command = ['ffmpeg', '-i', input_file, '-vn', '-acodec', 'pcm_s16le', '-ar', '44100', '-ac', '2', output_file]
    try:
        subprocess.run(command, check=True)
        print(f"Conversion successful: {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred during conversion: {e}")

convert_mp4_to_wav("first_test.mp4", "first_test.wav")
remove_first_n_seconds("first_test.wav", "first_test_trimmed.wav", 46)