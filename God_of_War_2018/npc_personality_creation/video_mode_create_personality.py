from langchain.llms import Cohere
from langchain import PromptTemplate, LLMChain
import json
import random
import names


def create_personality(game_name, gender, age, race):

    voice_list = json.load(open('default_voices/female_voices.json', 'r'))
    if gender == 'Man':
        voice_list = json.load(open('default_voices/male_voices.json', 'r'))

    # Generate random name
    name = names.get_full_name(gender=gender)

    # Select a voice
    selected_voice = random.choice(voice_list)['ShortName']

    # Randomly select an API key
    selected_key = json.load(open('apikeys.json', 'r'))['api_keys'][random.randint(
        0, len(json.load(open('apikeys.json', 'r'))['api_keys'])-1)]

    # Initialise model
    llm = Cohere(cohere_api_key=selected_key,
                 model='command', temperature=1.4, max_tokens=300)

    # Create the template string
    template = """Create a personality profile for Atreus (Age: 12-14, Gender: Male, Race: Demigod):
Atreus, the son of Kratos and a giantess named Faye, is a young demigod who navigates the harsh world of Norse mythology alongside his father. Although just a boy, Atreus exhibits a mix of curiosity, intelligence, and a strong moral compass. As he grows, he learns to balance his human emotions with his emerging god-like abilities. His journey is marked by the challenge of understanding his true identity, his powers, and his destiny."""

    # Create prompt
    prompt = PromptTemplate(template=template, input_variables=[
                            'name', 'age', 'race', 'gender'])

    # Create and run the llm chain
    llm_chain = LLMChain(prompt=prompt, llm=llm)
    bio = llm_chain.run(name=name, age=age, race=race, gender=gender)
    with open(f'{game_name}/characters/default/bio.txt', 'w') as file:
        file.write(bio)

    with open(f'{game_name}/characters/default/voice.txt', 'w') as file:
        file.write(selected_voice)

    with open(f'{game_name}/characters/default/name.txt', 'w') as file:
        file.write(name)

    return name, selected_voice
