from pytube import YouTube
import re
import os
import json

yt = YouTube("https://youtu.be/oWMNskk8nzY?si=plumQqVv8kA0PSgv")

audio_stream = yt.streams.get_audio_only()
audio_stream.download(output_path='', filename='first_test.mp4')


s = dict()

for v in vids:
    result = model.transcribe(f"nail_tips/{v}")
    s[v] = result["text"]

with open("nail_tips.json", "w", encoding="UTF-8") as outfile:
    json.dump(s, outfile)

