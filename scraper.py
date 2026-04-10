import requests
from bs4 import BeautifulSoup
import json
import os

def scrape_stories():
    # ৫টি ওয়েবসাইটের সাইটম্যাপ লিঙ্ক
    sitemaps = [
        "https://www.banglachotikahinii.com/post-sitemap.xml",
        "https://banglaxchotikahini.com/post-sitemap.xml",
        "https://bdsexstory.online/post-sitemap.xml",
        "https://chotigolpo.club/post-sitemap.xml",
        "https://www.banglapanugolpo.com/post-sitemap.xml",
        # Bakigulo eikhane add korun...
    ]
    
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    
    # Existing stories load kora (Duplicate check korar jonno)
    if os.path.exists('stories.json'):
        with open('stories.json', 'r', encoding='utf-8') as f:
            try:
                all_stories = json.load(f)
            except:
                all_stories = []
    else:
        all_stories = []

    existing_titles = {story['title'] for story in all_stories}
    new_stories_count = 0

    for sitemap_url in sitemaps:
        try:
            print(f"Fetching: {sitemap_url}")
            res = requests.get(sitemap_url, headers=headers, timeout=10)
            soup = BeautifulSoup(res.content, 'xml')
            links = [loc.text for loc in soup.find_all('loc')][1:10] # Proti site theke top 10 ta link

            for link in links:
                try:
                    story_res = requests.get(link, headers=headers, timeout=10)
                    story_soup = BeautifulSoup(story_res.text, 'html.parser')
                    
                    title = story_soup.find('h1').text.strip() if story_soup.find('h1') else None
                    
                    # Title jodi agei theke thake, tobe skip korbe
                    if not title or title in existing_titles:
                        continue
                    
                    content_div = story_soup.find('div', class_='entry-content') or story_soup.find('article')
                    if content_div:
                        for tag in content_div(['script', 'style', 'aside']): tag.decompose()
                        full_text = content_div.get_text(separator="\n").strip()
                        
                        new_story = {
                            "id": len(all_stories),
                            "title": title,
                            "content": full_text,
                            "author": "সংগৃহীত",
                            "source": sitemap_url.split('/')[2]
                        }
                        
                        all_stories.append(new_story)
                        existing_titles.add(title)
                        new_stories_count += 1
                        print(f"Added: {title}")
                except Exception as e:
                    print(f"Error scraping {link}: {e}")
                    
        except Exception as e:
            print(f"Sitemap Error {sitemap_url}: {e}")

    # Shob stories ekshathe save kora
    with open('stories.json', 'w', encoding='utf-8') as f:
        json.dump(all_stories, f, ensure_ascii=False, indent=4)
    
    print(f"Total {new_stories_count} new stories added!")

if __name__ == "__main__":
    scrape_stories()
    
