from additional_data.character_gpt_errors import *
from typing import Union
import json
import warnings
import os

jailbreak_dict={
    "default":"default.txt"
}
current_dir = os.path.dirname(os.path.abspath(__file__))
class GptPrompt:
    def __init__(self, **kwargs):
        if "import_data" in kwargs:
            self.__init_from_import_data(kwargs["import_data"])
        else:
            self.__init_from_parameters(**kwargs)

    def __init_from_parameters(self, **kwargs):
        if "jailbreak_type" in kwargs:
            jailbreak_txt=jailbreak_dict.get(kwargs["jailbreak_type"], None)
            if not jailbreak_txt:
                raise InvalidJailbreakType
            with open(os.path.join(current_dir,f"jailbreaks/{jailbreak_txt}"), "r", encoding="utf-8") as f:
                self._jailbreak_text = f.read()
        elif "custom_jailbreak" in kwargs:
            self._jailbreak_text=kwargs["custom_jailbreak"]
        else:
            raise JailbreakMessageIsNotProvided
        self._tokens_limit=kwargs.get("tokens_limit")
        self._average_tokens=kwargs.get("average_tokens")
        self._character_description = kwargs.get("character_description", {})
        self._initial_message = kwargs.get("story_initial_message")
        with open(os.path.join(current_dir,"additional_data/prompt_finish"), "r", encoding="utf-8") as f:
            self._prompt_end=f.read()
        self._debug_mode = kwargs.get("debug_mode", False)
        self._model_author=kwargs.get("model_author")
        self._user_name_for_story=kwargs.get("user_name")
        self._story_start_context=kwargs.get("story_start_context")

    def __init_from_import_data(self, import_data):
        self._jailbreak_text=import_data["jailbreak_text"]
        self._character_description = import_data["character_description"]
        self._initial_message = import_data["initial_message"]
        self._prompt_end = import_data["prompt_end"]
        self._tokens_limit=import_data.get("tokens_limit")
        self._average_tokens=import_data.get("average_tokens")
        self._debug_mode=import_data.get("debug_mode", False)
        self._user_name_for_story=import_data.get("user_name")
        self._story_start_context=import_data.get("story_start_context")
        self._model_author=import_data.get("model_author")


    def generate_prompt(self):
        tokens_limits=self._get_tokens_limitations()
        response=f"{self.jailbreak_text}{tokens_limits}{self.get_debug_mode_message()}\n"
        if self.user_name:
            response+=f"User name for current story: {self.user_name}\n"
        else:
            warnings.warn("User name for current story is not specified. All {{user}} will not be replaced by the username")
        if self.character_description:
            response+=self._generate_character_description()
        else:
            warnings.warn("You didn't provide character description")
        if self.initial_message:
            response+=f"This is your initial message that you need to start story from: (\"{self._initial_message}\")\n"
        else:
            warnings.warn("You didn't provide story initial message")
        if self.story_start_context:
            story_start_context=self.story_start_context
            if self.user_name:
                story_start_context=story_start_context.replace("{{user}}", self.user_name)
            response+=f"Story start context: (\"{story_start_context}\")\n"
        response+=self._prompt_end
        return response

    def get_debug_mode_message(self):
        if not self._debug_mode:
            return ""
        with open(os.path.join(current_dir,"additional_data/debug_mode_prompt"), "r") as f:
            return f.read()

    def _get_tokens_limitations(self):
        if self.tokens_limit:
            return f" Write your responses with maximum {self.tokens_limit} tokens long messages."
        elif self.average_tokens:
            return f" Write your responses with average {self.average_tokens} tokens long messages."
        else:
            return ""

    def generate_prompt_and_save_to_file(self, filename):
        with open(filename, "w", encoding="utf-8") as f:
            f.write(self.generate_prompt())

    def _generate_character_description(self):
        response="Your character description:\n"
        character_information_found=False
        for element in self.character_description:
            if element=="Character information":
                character_information_found=True
            if type(self.character_description[element])==list:
                element_data=" + ".join(f"\"{cur_element}\"" for cur_element in self.character_description[element])
            else:
                element_data=f"\"{self.character_description[element]}\""
            if self.user_name:
                element_data=element_data.replace("{{user}}", self.user_name)
            response+=f"{element}=({element_data})\n"
        if not character_information_found:
            warnings.warn("You didn't provide \"Character information\" field in character description")
        return response

    def add_description_parameter(self, key:str, value:Union[str, dict]):
        self.character_description[key]=value

    def add_description_parameters(self, parameters:dict):
        self.character_description.update(parameters)

    @staticmethod
    def import_existing_prompt(prompt_name: str=None, filename: str=None):
        if prompt_name:
            with open(os.path.join(current_dir,f"ready_to_use_prompts/{prompt_name}"), "r", encoding="utf-8") as f:
                prompt_data=json.loads(f.read())
        elif filename:
            with open(filename, "r", encoding="utf-8") as f:
                prompt_data = json.loads(f.read())
        else:
            raise PromptImportError
        return GptPrompt(import_data=prompt_data)

    def export_prompt(self, filename_to_save: str):
        response_data={
            "jailbreak_text":self.jailbreak_text,
            "character_description":self.character_description,
            "initial_message":self.initial_message,
            "prompt_end":self._prompt_end,
            "debug_mode": self.debug_mode
        }
        if self.story_start_context:
            response_data["story_start_context"]=self.story_start_context
        if self._average_tokens:
            response_data["average_tokens"]=self.average_tokens
        if self._tokens_limit:
            response_data["tokens_limit"] = self.tokens_limit
        if self.user_name:
            response_data["user_name"]=self.user_name

        if self._model_author:
            response_data["model_author"]=self.model_author
        with open(filename_to_save, "w", encoding="utf-8") as f:
            json.dump(response_data, f, ensure_ascii=False, indent=4)

    @property
    def character_description(self):
        return self._character_description

    @property
    def jailbreak_text(self):
        return self._jailbreak_text

    @property
    def initial_message(self):
        return self._initial_message

    @property
    def model_author(self):
        return self._model_author

    @property
    def average_tokens(self):
        return self._average_tokens

    @property
    def tokens_limit(self):
        return self._tokens_limit

    @property
    def debug_mode(self):
        return self._debug_mode

    @property
    def user_name(self):
        return self._user_name_for_story

    @property
    def story_start_context(self):
        return self._story_start_context





