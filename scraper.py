import requests
from bs4 import BeautifulSoup
import json
import os
import time

def scrape_stories():
    # সাইটম্যাপ লিঙ্কসমূহ
    sitemaps = [
        "https://www.banglachotikahinii.com/post-sitemap.xml",
        "https://banglaxchotikahini.com/post-sitemap.xml",
        "https://bdsexstory.online/post-sitemap.xml",
        "https://chotigolpo.club/post-sitemap.xml",
        "https://www.banglapanugolpo.com/post-sitemap.xml",
    ]
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    # Existing stories load kora (Duplicate check korar jonno)
    if os.path.exists('stories.json'):
        with open('stories.json', 'r', encoding='utf-8') as f:
            try:
                all_stories = json.load(f)
            except:
                all_stories = []
    else:
        all_stories = []

    # টাইটেল দিয়ে ডুপ্লিকেট চেক করার সেট
    existing_titles = {story['title'] for story in all_stories}
    new_stories_count = 0

    for sitemap_url in sitemaps:
        try:
            print(f"--- Fetching: {sitemap_url} ---")
            res = requests.get(sitemap_url, headers=headers, timeout=15)
            soup = BeautifulSoup(res.content, 'html.parser' if 'html' in res.headers.get('Content-Type', '') else 'xml')
            
            links = [loc.text.strip() for loc in soup.find_all('loc')]
            filtered_links = [l for l in links if "sitemap" not in l and l != sitemap_url][:15] 

            for link in filtered_links:
                try:
                    story_res = requests.get(link, headers=headers, timeout=15)
                    story_soup = BeautifulSoup(story_res.text, 'html.parser')
                    
                    title_tag = story_soup.find('h1')
                    title = title_tag.get_text().strip() if title_tag else None
                    
                    # Title না থাকলে বা আগে থেকে থাকলে স্কিপ
                    if not title or title in existing_titles:
                        continue
                    
                    content_div = (
                        story_soup.find('div', class_='entry-content') or 
                        story_soup.find('div', class_='post-content') or 
                        story_soup.find('article') or
                        story_soup.find('div', class_='td-post-content')
                    )

                    if content_div:
                        for tag in content_div(['script', 'style', 'aside', 'ins', 'header', 'footer']): 
                            tag.decompose()
                            
                        full_text = content_div.get_text(separator="\n").strip()
                        
                        if len(full_text) < 200: continue 

                        # এখানে কোনো সোর্স বা ইউআরএল সেভ হবে না
                        new_story = {
                            "title": title,
                            "content": full_text,
                            "author": "সংগৃহীত"
                        }
                        
                        all_stories.append(new_story)
                        existing_titles.add(title)
                        new_stories_count += 1
                        print(f"✅ Added: {title}")
                        
                        time.sleep(1) # সার্ভার সেফটি
                        
                except Exception as e:
                    print(f"❌ Error scraping link: {e}")
                    
        except Exception as e:
            print(f"⚠️ Sitemap Error: {e}")

    # ID রিসেট করে সিরিয়াল সাজানো
    for i, story in enumerate(all_stories):
        story['id'] = i

    # ডাটা সেভ করা
    with open('stories.json', 'w', encoding='utf-8') as f:
        json.dump(all_stories, f, ensure_ascii=False, indent=4)
    
    print(f"\n✨ Done! {new_stories_count} new stories added without source links.")

if __name__ == "__main__":
    scrape_stories()
                    
