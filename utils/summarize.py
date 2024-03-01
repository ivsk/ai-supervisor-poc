from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
import configparser
from utils.validator import BaseFile
import json
import os


class Summarizer(BaseFile):

    def __init__(self, path, openai_model):
        super().__init__(path)
        self.path = path
        self.openai_model = openai_model
        self.validate()

    def validate(self):
        valid_extensions = [".txt"]
        self._validate_extension(valid_extensions)

    def get_config(self):
        config = configparser.ConfigParser()
        config.read("config.ini")
        api_key = config.get("OPENAI", "ApiKey")
        metaprompt = config.get("METAPROMPT", "summarizer")
        return api_key, metaprompt

    def summarize(self):

        with open(self.path) as f:
            transcript = f.read()

        openai_key, metaprompt = self.get_config()
        prompt = ChatPromptTemplate.from_template(metaprompt)
        model = ChatOpenAI(model="gpt-4", openai_api_key=openai_key)

        output_parser = StrOutputParser()
        prompt_value = prompt.invoke({"sample": f"{transcript}"})
        message = model.invoke(prompt_value)
        output_dict = output_parser.invoke(message)
        with open(f"{os.path.splitext(self.path)[0]}.json", "w") as f:
            json.dump(output_dict)
