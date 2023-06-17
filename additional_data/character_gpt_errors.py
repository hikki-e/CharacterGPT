class InvalidJailbreakType(Exception):
    pass

class PromptImportError(Exception):
    def __init__(self):
        super().__init__("You didn't provide prompt_name or filename to import prompt")

class JailbreakMessageIsNotProvided(Exception):
    pass