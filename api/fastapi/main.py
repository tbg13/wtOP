from fastapi import FastAPI, Path, HTTPException
from typing import Optional

from pydantic import BaseModel
import json

from api_meta import Character, fill_character_class, path_to_characters_json, load_json
    
app = FastAPI()

@app.get("/characters/{character_names}")
def create_character(character_names: str):
    character_names_list = character_names.split('&')
    characters = {}
    
    #character_data = load_json(f'{path_to_characters_json}/latest_characters.json')
    character_data = load_json('/app/scrap/data/latest_characters.json')
    
    for name in character_names_list:
        #if name not in character_names_list: #TODO: good idea but dumb execution, doesn't work
        #    raise HTTPException(status_code=404, detail=f'Character {name} not found in database')

        character = fill_character_class(name.lower(), character_data)
        characters[name] = character
    
    return characters