from pyannote.audio import Pipeline
import torchaudio
import configparser

config = configparser.ConfigParser()

config.read("config.ini")
api_key = config.get("HUGGINGFACE", "ApiKey")
pipeline = Pipeline.from_pretrained(
  "pyannote/speaker-diarization-3.1",
  use_auth_token=api_key)

diarization = pipeline("first_test.mp4")

with open("first_test.rttm", "w") as rttm:
  diarization.write_rttm(rttm)

from pyannote.audio.pipelines.utils.hook import ProgressHook
with ProgressHook() as hook:
    diarization = pipeline("first_test.mp4", hook=hook)

