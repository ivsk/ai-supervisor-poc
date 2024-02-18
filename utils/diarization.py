from pyannote.audio import Pipeline
import torchaudio
import configparser
import torch
import whisper
from transformers import pipeline
from speechbox import ASRDiarizationPipeline



config = configparser.ConfigParser()

config.read("config.ini")
api_key = config.get("HUGGINGFACE", "ApiKey")
pipeline = Pipeline.from_pretrained(
  "pyannote/speaker-diarization-3.1",
  use_auth_token=api_key)

pipeline.to(torch.device("cuda"))

diarization = pipeline("first_test_trimmed.wav", num_speakers=2)

with open("first_test.rttm", "w") as rttm:
  diarization.write_rttm(rttm)

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

asr_pipeline = pipeline(
    "automatic-speech-recognition",
    model="openai/whisper-large",
)

asr_pipeline(
    sample["audio"].copy(),
    generate_kwargs={"max_new_tokens": 256},
    return_timestamps=True,
)

pipeline = ASRDiarizationPipeline(
    asr_pipeline=asr_pipeline, diarization_pipeline=diarization_pipeline
)
