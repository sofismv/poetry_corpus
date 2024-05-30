import requests
from bs4 import BeautifulSoup
import time
from tqdm import tqdm
import json

base_url = 'https://slova.org.ru'
poets_url = f'{base_url}/serebryanyj-vek/'

def get_page_content(url)
    response = requests.get(url)
    response.raise_for_status()
    return response.text

def extract_links(content):
    soup = BeautifulSoup(content, 'html.parser')
    links = soup.select('a[href]')
    all_links = {
        link.get_text(): base_url + link['href']
        for link in links
        if not '/serebryanyj-vek/' in link['href'] and link.parent.name == 'div'
    }
    return all_links

def extract_poem_text(poem_page_content):
    soup = BeautifulSoup(poem_page_content, 'html.parser')
    poem_text=''
    p_tag = soup.find('p')
    if p_tag:
        poem_text = p_tag.get_text()
    if not poem_text:
        pre_tag = soup.find('pre')
        if pre_tag:
            poem_text = pre_tag.get_text()    
    return poem_text

def scrape_poems():
    poets_page_content = get_page_content(poets_url)
    poet_links = extract_links(poets_page_content)

    all_poems = []
    poet_cnt = 0
    
    for poet, link in poet_links.items():
        poet_cnt+=1
        print(f"scraping poems of {poet}...")
        poet_page_content = get_page_content(link)
        poem_links = extract_links(poet_page_content)
        
        for title, poem_link in tqdm(poem_links.items()):
            poem_page_content = get_page_content(poem_link)
            poem_text = extract_poem_text(poem_page_content)
            all_poems.append({'poet':poet, 'title':title, 'poem':poem_text})
            time.sleep(0.1)
        if poet_cnt == 1:
            break
        time.sleep(1)
    
    return all_poems

if __name__ == '__main__':
    poems = scrape_poems()
    with open('poems.json', 'w') as file:
        json.dump(poems, file)