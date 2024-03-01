from utils.process_audio import AudioProcessor
from utils.downloader import Downloader
from utils.transcribe import Transcriber
from utils.summarize import Summarizer
import argparse


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="SupervisorAI data prep POC",
        description="This is a helper CLI tool for processing either youtube videos or audio files into question-answer pairs that can be used for fine-tuning an LLM model."
    )
    subparsers = parser.add_subparsers(dest='command')

    # Downloader
    parser_downloader = subparsers.add_parser('downloader', help='Download audio from a YouTube URL')
    parser_downloader.add_argument('url', type=str, help='A valid YouTube video URL')

    # Audio processor
    parser_audioprocessor = subparsers.add_parser('audioprocessor', help='Process audio')
    parser_audioprocessor.add_argument('file_path', type=str, required=True, help='Path to the audio file you wish to trim')
    parser_audioprocessor.add_argument('trim_type', type=str, choices=['start', 'end'], help='Type of trimming')
    parser_audioprocessor.add_argument('seconds', type=int, help='Number of seconds to trim')


    # Transcriber
    parser_transcriber = subparsers.add_parser('transcriber', help='Transcribe audio files')
    parser_transcriber.add_argument('file_path', type=str, help='Path to the audio file to be transcribed')

    # Summarizer
    parser_summarizer = subparsers.add_parser('summarizer', help='Summarize transcriptions')
    parser_summarizer.add_argument('file_path', type=str, help='Path to the text file to be summarized')
    parser_summarizer.add_argument('model_type', type=str, choices=['gpt-4', 'gpt-3.5'], help='Type of model to use for summarization')

    args = parser.parse_args()

    if args.command == "downloader":
        downloader = Downloader(args.file_path)

    if args.command == "audioprocessor":
        processor = AudioProcessor(args.file_path)
        if args.type == "start" and args.seconds > 0:
            processor.remove_first_n_seconds(args.seconds)
        elif args.type == "end" and args.seconds > 0:
            processor.remove_last_n_seconds(args.seconds)

    elif args.command == 'transcriber':
        transcriber = Transcriber(args.file_path)
        print(f"Transcribing {args.file_path}")
        Transcriber.transcribe()

    elif args.command == 'summarizer':
        summarizer = Summarizer(args.file_path, args.model_type)
        print(f"Summarizing {args.file_path} with model {args.model_type}")
        Summarizer.summarize()
