### Workflow
import requests 
from bs4 import BeautifulSoup 

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

charac_name = "Alpaca"
charac_url = f"https://onepiece.fandom.com/wiki/{charac_name}"

r = requests.get(charac_url) 
soup = BeautifulSoup(r.content, 'html5lib')
print(soup.div)
# Add some logging / wait time

