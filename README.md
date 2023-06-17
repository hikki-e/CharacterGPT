# CharacterGPT
This library is designed to make the creation of characters for rollplay in ChatGPT much easier

# Installation

    pip install charactergpt-prompts

# Usage

## Create character from scratch

```python
from charactergpt_prompts.prompt_generator import GptPrompt

prompt_example=GptPrompt(**kwargs)
```
currently supported parameters:
- jailbreak_type(str) #Use one of the premade jailbreaks
  - default
- custom_jailbreak(str) #Pass your own jailbreak
- character_description(dict) #Dictionary of character characteristics
  - Note: For better results, you should add "Name" and "Character information"
- story_initial_message(str) #String containing the beginning of the story
- story_start_context(str) #Context of the beginning of the story so model can better understands where she is
- user_name(str) #Name of the character the user will play
  - Note: all {{user}} in character_description, story_initial_message and story_start_context will be replaced by this parameter
- tokens_limit(int) #Limit the number of tokens to be generated
- average_tokens(int) #Less strict token limit
- debug_mode(bool) #Adds the ability for the user to update the behavior of the model during role-play
  - Note: to call debug mode simply write DebugMode: before changes that you want to make
- model_author #Model author data


- import_data(dict) #If this parameter passed it will try to load prompt data from it


## Import existing character

```python
from charactergpt_prompts.prompt_generator import GptPrompt

example_prompt=GptPrompt.import_existing_prompt(prompt_name="Sakura")
#or
example_prompt=GptPrompt.import_existing_prompt(filename="example.json")
```
Note: if you pass prompt_name as a parameter it will import character from character examples folder  
List of "ready to go" characters:
- Alys
- Ami
- Sakura

## Update prompt parameters
```python
from charactergpt_prompts.prompt_generator import GptPrompt

example_prompt=GptPrompt.import_existing_prompt(prompt_name="Sakura")

#update jailbreak message
example_prompt.jailbreak_text="new jailbreak text"

#character description
example_prompt.character_description["Name"]="Ami"

#or if you want to update multiple parameters
description_extension={
    "Age":"23",
    "Dislikes":["being rude", "sadness", "when {{user}} is angry"]
}
example_prompt.add_description_parameters(description_extension)

#initial message
example_prompt.initial_message="new initial message"

#story start context
example_prompt.story_start_context="new story start context"

#user name
example_prompt.user_name="New user"

#tokens limit
example_prompt.tokens_limit=100
#avarage tokens
example_prompt.average_tokens=150

#debug mode
example_prompt.debug_mode=True

#model author
example_prompt.model_author="New model author"
```


## Export prompt as txt

```python
print(prompt_example.generate_prompt())
#or
prompt_example.generate_prompt_and_save_to_file("example.txt")
```

## Export prompt as json

```python
prompt_example.export_prompt("example.json")
```