# Data preprocessing CLI tool

This CLI tool supports 

## Installation

Ensure Python 3.10 is installed on your machine. Clone the repo and install the dependencies in the requirements.txt file.


## Usage

The tool has four main commands:

### 1. Downloader

Download audio from a YouTube URL.

```bash
python main.py downloader --url <YouTube_URL>
```

### 2. AudioProcessor

Trim an audio file by specifying the file path, trimming type ('start' or 'end'), and the number of seconds.

```bash
python main.py audioprocessor --file_path <file_path> --trim_type <trim_type> --seconds <seconds>
```

### 3. Transcriber
Transcribe an audio file to text by specifying the file path.
#### Important: the transcriber model currently implemented in this tool is the whisper-large which requires significant amount of GPU memory. If you don't have CUDA capable GPU in your system, the transcriber will utilize your CPU which is significantly slower compared to GPU.

```bash
python main.py transcriber --file_path <file_path>
```

### 4. Summarizer
You can use the summerizer tool to pass a transcribed text to a selected OpenAI GPT model and summarize it.
#### IMPORTANT In order to use this script, you MUST have a valid OpenAI API key stored in a config.ini file in your working directory in the following way

```
[OPENAI]
ApiKey = yourapikey
```
#### In addition, you must also store an instruction prompt in the config.ini file that the script will pass to the OpenAi endpoint. The prompt below is an example intended to summarize counsellor-supervisor conversation into a single question-answer pair.
```
[METAPROMPT]
summarizer = Your task is to identify the counsellor and supervisor in the conversation. Summarize the conversation into only one
 round of conversation, one query or description by the patient and one feedback by the counsellor.
 counsellor's description and supervisor’s feedback should be detailed, and both description and feedback should be more
 than 50 words. The feedback should include the supervisor's answer. If the counsellor shows worry or complain, can ask
 only one additional question for more further details, but it should all in one feedback. If the counsellor says he or she becomes
 better, the supervisor cannot ask question.
 Include all of those in only one round of conversation, one by counsellor and one by the supervisor
 Output format should be a json in following format:
 key1: "instruction", and value1: "If you are a supervisor, please answer the questions based on the description of the counsellor.",
 key2: "input", and value2: "counsellor's description from first-person view",
 key3: "output", and value3: "supervisor's feedback from first-person view"
 Conversation: {sample}
```

### End to end example input and output:
For the following YouTube video https://youtu.be/o6AdcHbVujg?si=z5cqN3vzt0hhpkqn
After transcription, the aforementioned prompt produced the following output:
```
{"instruction": "If you are a supervisor, please answer the questions based on the description of the counsellor.",
 "input": "I have been working with a client named Shannon, and our sessions are going quite well. However, I've noticed that I've started to think about her more than my other clients, sometimes even when I'm with other clients or when I'm at home. I think I'm starting to have feelings for her. When she misses appointments, I feel disappointed. She's one of my favorite clients and when she comes in, it improves my day. I'm worried about this situation because I don't want to jeopardize our professional relationship or my career.",
 "output": "Your experience is not uncommon, but it's crucial to address it appropriately to protect everyone involved. It's great that you've brought this to my attention, it shows courage and trust. Regarding your feelings for your client, you need to remember that any type of romantic relationship with a client or their close ones is strictly prohibited. It's essential for maintaining your professional reputation and avoiding legal issues. I suggest that you start counseling yourself to process your feelings. I will reassign Shannon to another counselor to avoid possible complications. We will meet more frequently until we navigate this situation. Remember, your commitment to this field is admirable, and your awareness of your feelings is a step in the right direction."}
```

Disclaimer: the prompt used in the example is a modified version of a prompt used in the article cited below.
## References

- Liu, J. M., Li, D., Cao, H., Ren, T., Liao, Z., & Wu, J. (2023). Chatcounselor: A large language models for mental health support. arXiv preprint arXiv:2309.15461. Available at: [https://arxiv.org/abs/2309.15461](https://arxiv.org/abs/2309.15461)
