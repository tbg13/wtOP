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

import json, os

def append_to_json(file_path, data, overwrite=False):
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError
        
        with open(file_path, 'r+') as file:
            existing_data = json.load(file)
            
            character_name = data['character']['name'].lower() #super important to lower for future usage in api !!
            
            if overwrite:
                # Replace the existing entry with the same key
                existing_data[character_name] = data
            else:
                if character_name in existing_data:
                    raise ValueError(f"Character {character_name} already exists. Use overwrite=True to replace.")
                else:
                    existing_data[character_name] = data
            
            file.seek(0)  # Move the cursor to the start of the file
            file.truncate()  # Clear the file content
            json.dump(existing_data, file, indent=3)
    except FileNotFoundError:
        character_name = data['character']['name'].lower() # lower key; edge case when creating new file
        with open(file_path, 'w') as file:
            json.dump({character_name: data}, file, indent=3)
