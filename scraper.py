import requests
from bs4 import BeautifulSoup
import json
import os

def scrape_multipage_site(base_url, pages=3):
    all_stories = []
    for page in range(1, pages + 1):
        try:
            # Example: https://site.com/stories?page=1
            url = f"{base_url}?page={page}" 
            res = requests.get(url, timeout=10)
            soup = BeautifulSoup(res.text, 'html.parser')
            
            # Website er structure onujayi selector dite hobe
            items = soup.find_all('article', class_='post-item') 
            
            for item in items:
                title = item.find('h2').text.strip()
                content = item.find('p').text.strip()
                link = item.find('a')['href']
                
                all_stories.append({
                    "title": title,
                    "content": content,
                    "link": link,
                    "source": base_url.split('//')[1].split('/')[0]
                })
            print(f"Scraped page {page} from {base_url}")
        except Exception as e:
            print(f"Error on {url}: {e}")
            break
    return all_stories

def main():
    # Jey jey site theke collect korben tader list
    target_sites = [
        "https://banglaxchotikahini.com/",
        "https://chotigolpo.club/"
    ]
    
    final_data = []
    for site in target_sites:
        # Prottek site er 5 page porjonto collect korbe
        site_data = scrape_multipage_site(site, pages=5) 
        final_data.extend(site_data)

    # Purono data jate harale na jay, sheta handle kora
    file_path = 'stories.json'
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            old_data = json.load(f)
            # Notun ar purono data merge kora (Duplicate bad diye)
            existing_titles = {s['title'] for s in old_data}
            for story in final_data:
                if story['title'] not in existing_titles:
                    old_data.append(story)
            final_data = old_data

    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(final_data, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    main()
