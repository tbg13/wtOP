from fastapi import FastAPI, Path, HTTPException
from typing import Optional

from pydantic import BaseModel

from datetime import datetime

import json

path_to_characters_json = '/app/scrap/data'

class Character(BaseModel):
    character_name: str
    overview: Optional[dict] = None
    details: Optional[dict] = None
    last_updated: datetime = datetime.now()

def load_json(file_path: str):
    with open(file_path, 'r') as file:
        return json.load(file)

def fill_character_class(name, character_data):
    character_info = character_data[name]
    
    character = Character(
        character_name = name
        , overview = character_info['character'].get('overview', {})
        , details = character_info['character'].get('details', {})
        , last_updated = character_info['scrap_datetime']
    )
    
    return character
        
    