category_mappings = {
    "appearance": ["Appearance", "Appearances", "Looks"],
    "personality": ["Personality", "Character"],
    "abilities_and_powers": ["Abilities and Powers", "Abilities", "Powers"],
    "devil_fruit": ["Devil Fruit"],
    "anime_only_techniques": ["Anime-Only Techniques"],
    "weapons": ["Weapons"],
    "haki": ["Haki"],
    "history": ["History"],
    "wano_country_arc": ["Wano Country Arc"],
    "major_battles": ["Major Battles"],
    "references": ["References"]
}

list_of_characters = []

import json

def append_to_json(file_path, data):
    try:
        with open(file_path, 'r+') as file: #open json in read/write
            existing_data = json.load(file)
            existing_data.append(data)
            file.seek(0) #ensures updated data overwrites old data, without it updated data is appended after old data > duplicates everything
            json.dump(existing_data, file, indent=3)
    except FileNotFoundError: #when the file doesn't exist
        with open(file_path, 'w') as file:
            json.dump([data], file, indent=3)
            