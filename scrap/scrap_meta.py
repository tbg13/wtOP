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

def append_to_json(file_path, data, overwrite=False):
    try:
        with open(file_path, 'r+') as file:
            existing_data = json.load(file)
            
            if overwrite:
                # Find and replace the existing entry with the same key
                for i, entry in enumerate(existing_data):
                    if entry['character']['name'] == data['character']['name']:
                        existing_data[i] = data
                        break
                else:
                    existing_data.append(data)  # If not found, append as new data
            else:
                existing_data.append(data)
            
            file.seek(0)  # Move the cursor to the start of the file
            file.truncate()  # Clear the file content
            json.dump(existing_data, file, indent=3)
    except FileNotFoundError:
        with open(file_path, 'w') as file:
            json.dump([data], file, indent=3)