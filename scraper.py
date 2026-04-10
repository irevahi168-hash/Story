import requests
from bs4 import BeautifulSoup
import json
import os

def scrape_from_xml():
    # এখানে আপনার টার্গেট ওয়েবসাইটের সাইটম্যাপ (Sitemap XML) লিঙ্ক দিন
    xml_url = "https://banglaxchotikahini.com/post-sitemap.xml" 
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    try:
        print("Fetching XML...")
        response = requests.get(xml_url, headers=headers)
        # XML ফাইল পার্স করা
        soup = BeautifulSoup(response.content, 'xml')
        
        # XML থেকে সব <loc> ট্যাগ (লিঙ্ক) বের করা
        all_links = [loc.text for loc in soup.find_all('loc')]
        print(f"Total links found: {len(all_links)}")

        stories = []
        # আমরা প্রথম ১০-১৫টি লিঙ্কে ঢুকে গল্প কালেক্ট করব (বেশি নিলে টাইম আউট হতে পারে)
        for index, link in enumerate(all_links[1:15]): 
            try:
                print(f"Scraping link: {link}")
                res = requests.get(link, headers=headers)
                story_soup = BeautifulSoup(res.text, 'html.parser')
                
                # টাইটেল এবং কন্টেন্ট খোঁজা (সাইট ভেদে এই ক্লাসগুলো পাল্টাতে হতে পারে)
                title = story_soup.find('h1').text.strip() if story_soup.find('h1') else "শিরোনামহীন"
                
                # গল্পের মেইন বডি খোঁজা
                content_div = story_soup.find('div', class_='entry-content') or story_soup.find('article')
                if content_div:
                    # প্রথম ৫০০ ক্যারেক্টার নেওয়া হচ্ছে প্রিভিউ হিসেবে
                    content = content_div.text.strip()[:600] + "..."
                else:
                    content = "বিস্তারিত গল্পের লিঙ্কে গিয়ে পড়ুন।"

                stories.append({
                    "id": index,
                    "title": title,
                    "content": content,
                    "link": link,
                    "author": "সংগৃহীত",
                    "source": "XML Bot"
                })
            except Exception as e:
                print(f"Error scraping {link}: {e}")
                continue

        # JSON ফাইলে সেভ করা
        if stories:
            with open('stories.json', 'w', encoding='utf-8') as f:
                json.dump(stories, f, ensure_ascii=False, indent=4)
            print(f"Successfully saved {len(stories)} stories to stories.json")
        else:
            print("No stories were collected.")

    except Exception as e:
        print(f"Main XML Error: {e}")

if __name__ == "__main__":
    scrape_from_xml()
    
