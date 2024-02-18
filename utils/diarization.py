from pyannote.audio import Pipeline
import torchaudio
import configparser
import torch
import whisper
from whisperx import load_align_model, align
from whisperx.diarize import assign_word_speakers

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

model_name = "large"
model = whisper.load_model(model_name, DEVICE)
script = model.transcribe("first_test_trimmed.wav")

model_a, metadata = load_align_model(language_code=script["language"], device=DEVICE)
script_aligned = align(script["segments"], model_a, metadata, "first_test_trimmed.wav", DEVICE)

# Align Speakers
result_segments, word_seg = list(assign_word_speakers(
    diarization, script_aligned).values())
transcribed = []
for result_segment in result_segments:
    transcribed.append(
        {
            "start": result_segment["start"],
            "end": result_segment["end"],
            "text": result_segment["text"],
            "speaker": result_segment["speaker"],
        }
    )