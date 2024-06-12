### Workflow
import requests, re, json
from bs4 import BeautifulSoup 
from datetime import datetime

from scrap_meta import category_mappings, list_of_characters, append_to_json

## A) Scrape https://onepiece.fandom.com/wiki/List_of_Canon_Characters for list of links towards all canon characters

## B) Get rid of the fluff and save the html output for caching purposes (no overloading)

## C) Scrape page as json based on Content
### 1 Appearance
### 2 Personality
### 3 Abilities and Powers | Abilities | Power
### 4 History
### 5 References

## C) Scrape for the Statistics and Devil Fruit informations (pi-items)

#Test run with Alpaca


#print(soup.div)
#Todo: Add some logging / wait time

def toc_to_json(tocs):
    """
    Scrap table of content and returns a json.

    Args:
        tocs (str): html soup of table of contents, filtered through class patterns

    Returns:
        json
        
    Remarks:
        #find_all recursive=False to only consider direct children and avoid dup entries with nested children

    """
    
    toc_data = []
    for li in tocs:
        entry = {
            'name': li.find('span', class_='toctext').get_text(),
            'children': toc_to_json(li.find('ul').find_all('li', recursive=False) if li.find('ul') else []) #recursive bs
        }
        toc_data.append(entry)
    return toc_data

def extract_text_with_spacing(element):
    text = ""
    last_text = ""
    
    for child in element.descendants:
        if child.name == 'a':
            # Extract text from hyperlink with surrounding spaces
            hyperlink_text = ' ' + child.get_text(strip=True) + ' '
            # Add hyperlink text if it's not a duplicate of the last added text
            if hyperlink_text.strip() != last_text.strip():
                text += hyperlink_text
                last_text = hyperlink_text
        elif child.string:
            # Extract text from non-hyperlink elements
            child_text = child.string
            # Add child text if it's not a duplicate of the last added text
            if child_text.strip() != last_text.strip():
                text += child_text
                last_text = child_text

    # Clean up extra spaces around punctuation and possessives
    text = re.sub(r'\s+([.,!?\'":;])', r'\1', text)  # Remove space before punctuation
    text = re.sub(r'([\'":;])\s+', r'\1 ', text)  # Ensure space after punctuation
    text = re.sub(r'(\w)\'s', r'\1\'s', text)  # Remove space before 's for possessives
    text = re.sub(r'\(\s+', '(', text)  # Remove space after opening parenthesis
    text = re.sub(r'\s+\)', ')', text)  # Remove space before closing parenthesis
    text = re.sub(r'\[\s+', '[', text)  # Remove space after opening square bracket
    text = re.sub(r'\s+\]', ']', text)  # Remove space before closing square bracket
    
    # Fix the issue with backslashes before apostrophes
    text = text.replace("\\'", "'")
    
    # Clean up extra spaces
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text
def enrich_toc(toc_data, soup):
    content_data = []
    for item in toc_data: 
        
        #TODO: Skip Site navigation or clean after ? Implemented for now, but need to decide. Maybe better to skip if need to add tables in the future (site nav data is in tables)
        if item['name'].lower() == 'site navigation':
            continue
        
        content_id = item['name'].replace(" ", "_")
        heading = soup.find(id = content_id).parent
        content_text = ""
        
        def process_sibling(sibling):
            nonlocal content_text
            # Next section is a paragraph
            if sibling.name == 'p':
                content_text += extract_text_with_spacing(sibling) + " "
            # Next section is an unordered or ordered list
            elif sibling.name in ['ul', 'ol']:
                for li in sibling.find_all('li'):
                    content_text += extract_text_with_spacing(li) + " "
            # Edge case if next section is a div, access it then run the above
            elif sibling.name == 'div':
                for sub_sibling in sibling.children:
                    process_sibling(sub_sibling)
        
        for sibling in heading.find_next_siblings():
            # Next section is a new heading, i.e. current is finished or empty
            if sibling.name in ['h2', 'h3', 'h4', 'h5', 'h6']:
                break
            process_sibling(sibling)
            
        content_entry = {
            'name': item['name'],
            'content': content_text.strip(),
            'children': enrich_toc((item['children'] if item['children'] else []), soup) #recursive bs
        }
        
        content_data.append(content_entry)
            
    return content_data

def normalize_key(key, mappings):
    for standard, synonyms in mappings.items():
        if key in synonyms:
            return standard
    return key.lower().replace(" ", "_")  # default conversion for unmapped categories
def process_item(item, mappings):
    category_name = normalize_key(item['name'], mappings)
    content = item.get("content", "").strip()
    subcategories = item.get("children", [])
    
    processed = [content]
    
    for subcat in subcategories:
        subcat_name = normalize_key(subcat['name'], mappings)
        subcat_content = process_item(subcat, mappings)
        
        if len(subcat_content) == 1:
            processed.append({subcat_name: subcat_content})
        else:
            if isinstance(processed[-1], dict) and subcat_name in processed[-1]:
                processed[-1][subcat_name].extend(subcat_content)
            else:
                processed.append({subcat_name: subcat_content})
    
    return processed
def transform_json(character_name, data, mappings):
    normalized_data = {
        "name": f"{character_name}",
        "overview": {},  # Add overview data when I come around to doing it, fckng done with scraping
        "details": {}
    }
    
    details = {}
    for item in data:
        category_content = process_item(item, mappings)
        category_name = normalize_key(item['name'], mappings)
        if category_name in details:
            details[category_name].extend(category_content)
        else:
            details[category_name] = category_content

    normalized_data["details"] = details
    
    return normalized_data

def scrap_character(character_name, category_mappings):
    character_url = f"https://onepiece.fandom.com/wiki/{character_name}"
    
    r = requests.get(character_url) 
    soup = BeautifulSoup(r.content, 'html5lib')
    print(f'{character_name}: scrapped')
    
    toc_pattern = re.compile(r'toclevel-1.*')
    tocs = soup.find_all("li", class_=toc_pattern)
    toc_data = toc_to_json(tocs)
    content_data = enrich_toc(toc_data, soup)
    normalized_json = transform_json(character_name, content_data, category_mappings)
    print(f'{character_name}: cleaned and normalized')
    
    character_data = {f'character': normalized_json, 'scrap_datetime': datetime.now().isoformat()}
    append_to_json('data/history_characters.json', character_data, overwrite=False)
    append_to_json('data/latest_characters.json', character_data, overwrite=True)

    print(f'{character_name}: added to character_json')

    #print(json.dumps(normalized_json, indent=3))
    
scrap_character('Crocodile', category_mappings)