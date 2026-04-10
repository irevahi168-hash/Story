import requests
from bs4 import BeautifulSoup
import json
import os

def scrape_full_stories():
    # XML/Sitemap লিঙ্ক
    xml_url = "https://banglaxchotikahini.com/post-sitemap.xml" 
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    
    try:
        print("Fetching Sitemap...")
        response = requests.get(xml_url, headers=headers)
        soup = BeautifulSoup(response.content, 'xml')
        
        # প্রথম ৫-১০টি গল্পের লিঙ্ক নিচ্ছি (বেশি নিলে ফাইল সাইজ অনেক বড় হয়ে যাবে)
        all_links = [loc.text for loc in soup.find_all('loc')][1:8] 

        stories = []
        for index, link in enumerate(all_links):
            try:
                print(f"Scraping Full Story: {link}")
                res = requests.get(link, headers=headers)
                story_soup = BeautifulSoup(res.text, 'html.parser')
                
                title = story_soup.find('h1').text.strip() if story_soup.find('h1') else "শিরোনামহীন"
                
                # গল্পের পুরো বডি কালেক্ট করা
                content_div = story_soup.find('div', class_='entry-content')
                if content_div:
                    # অপ্রয়োজনীয় ট্যাগ (বিজ্ঞাপন, সোশ্যাল শেয়ার) মুছে ফেলা
                    for tag in content_div(['script', 'style', 'aside', 'ins']):
                        tag.decompose()
                    
                    # পুরো গল্পটি নেওয়া হচ্ছে
                    full_text = content_div.get_text(separator="\n").strip()
                else:
                    full_text = "দুঃখিত, গল্পের লেখাটি পাওয়া যায়নি।"

                stories.append({
                    "id": index,
                    "title": title,
                    "content": full_text, # এখানে এখন পুরো গল্প থাকবে
                    "author": "সংগৃহীত",
                    "source": "গল্পের আসর"
                })
            except Exception as e:
                print(f"Error: {e}")
                continue

        # JSON ফাইলে সেভ করা
        with open('stories.json', 'w', encoding='utf-8') as f:
            json.dump(stories, f, ensure_ascii=False, indent=4)
        print("Done! Full stories saved.")

    except Exception as e:
        print(f"Main Error: {e}")

if __name__ == "__main__":
    scrape_full_stories()
