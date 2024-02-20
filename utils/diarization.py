from pyannote.audio import Pipeline
import torchaudio
import configparser
import torch
import whisper
from transformers import pipeline
from speechbox import ASRDiarizationPipeline
from sortedcontainers import SortedDict

def sorted_dict_to_json(sorted_dict):
    sorted_dict = sorted_dict
    result_list = []

    for segment, info in sorted_dict.items():
        start, end = segment.start, segment.end

        # Iterate through the dictionary items for each segment
        for track, label in info.items():
            result_list.append({
                'segment': {'start': start, 'end': end},
                'track': track,  # Now uses the actual track from the dictionary
                'label': label
            })
    return result_list


config = configparser.ConfigParser()

config.read("config.ini")
api_key = config.get("HUGGINGFACE", "ApiKey")
diarization_pipeline = Pipeline.from_pretrained(
  "pyannote/speaker-diarization-3.1",
  use_auth_token=api_key)

diarization_pipeline.to(torch.device("cuda"))

diarization = diarization_pipeline("first_test_trimmed.wav", num_speakers=2)

a = sorted_dict_to_json(diarization._tracks)

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

asr_pipeline = pipeline(
    "automatic-speech-recognition",
    model="openai/whisper-large",
    device=0
)

asr_pipeline(
    "first_test_trimmed.wav",
    generate_kwargs={"max_new_tokens": 256},
    return_timestamps=True
)

pipeline = ASRDiarizationPipeline(
    asr_pipeline=asr_pipeline, diarization_pipeline=diarization_pipeline
)
pipeline("first_test_trimmed.wav")
