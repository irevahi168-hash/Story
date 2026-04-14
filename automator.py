import os
import re

# কনফিগারেশন
HOME_PAGE = 'index.html'
MARKER = ""
AD_CODE = """
<div class="my-6 text-center">
    <script type="text/javascript">
        atOptions = { 'key' : '5e1e647770544994278e05a287ff9727', 'format' : 'iframe', 'height' : 50, 'width' : 320, 'params' : {} };
    </script>
    <script type="text/javascript" src="https://www.highperformanceformat.com/5e1e647770544994278e05a287ff9727/invoke.js"></script>
</div>
"""

def extract_info(content):
    # টাইটেল খুঁজে বের করা (পைப் '|' চিহ্নের আগের অংশটুকু নেবে)
    title_match = re.search(r'<title>(.*?)</title>', content, re.IGNORECASE)
    title = "নতুন গল্প"
    if title_match:
        full_title = title_match.group(1)
        title = full_title.split('|')[0].strip()

    # মূল গল্পের টেক্সট খুঁজে বের করা (story-text ডিভ এর ভেতর থেকে)
    story_match = re.search(r'<div class="story-text.*?">(.*?)</div>', content, re.DOTALL | re.IGNORECASE)
    story_body = story_match.group(1).strip() if story_match else ""
    
    return title, story_body

def process_files():
    if not os.path.exists(HOME_PAGE):
        return

    with open(HOME_PAGE, 'r', encoding='utf-8') as f:
        home_content = f.read()

    # বর্তমান ফোল্ডারের সব HTML ফাইল চেক করা
    all_files = [f for f in os.listdir('.') if f.endswith('.html') and f not in [HOME_PAGE, 'story-details.html', 'generator.html', 'automator.py']]

    for file_name in all_files:
        if file_name not in home_content:
            with open(file_name, 'r', encoding='utf-8') as f:
                raw_content = f.read()

            title, body = extract_info(raw_content)

            # আপনার দেওয়া এক্সাক্ট লেআউট
            new_layout = f"""<!DOCTYPE html>
<html lang="bn">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - Bangla CHOTI golpo Panu golpo</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Anek+Bangla:wght@300;400;700&display=swap" rel="stylesheet">
    <style>
        body {{ font-family: 'Anek Bangla', sans-serif; background-color: #f9f5f0; line-height: 1.8; }}
        .content-area {{ max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); }}
    </style>
</head>
<body class="text-gray-800">

    <nav class="bg-[#4a2c10] text-white p-4 sticky top-0 z-50 shadow-lg text-center font-bold">
        <a href="index.html" class="text-xl">Bangla <span class="text-amber-400">Choti</span> Panu</a>
    </nav>

    <main class="container mx-auto py-10 px-4">
        <div class="content-area">
            <h1 class="text-3xl md:text-4xl font-bold text-[#603813] mb-6 border-b pb-4">{title}</h1>
            {AD_CODE}
            <div class="story-text text-lg text-gray-700">
            {body}
            </div>
            {AD_CODE}
            <div class="mt-10 pt-6 border-t text-center">
                <a href="index.html" class="bg-[#603813] text-white px-8 py-3 rounded-full font-bold hover:bg-[#4a2c10] transition inline-block">আরো গল্প পড়ুন</a>
            </div>
        </div>
    </main>

    <footer class="bg-[#1a1108] text-gray-400 py-8 px-4 text-center mt-10">
        <p class="text-xs">Developed with ❤️ by Kabir</p>
    </footer>

</body>
</html>"""

            with open(file_name, 'w', encoding='utf-8') as f:
                f.write(new_layout)

            # হোমপেজে নতুন লিঙ্ক কার্ড
            new_card = f"""
    <article class="story-card bg-white p-6 rounded-2xl border border-gray-100 shadow-sm mb-4">
        <h2 class="text-xl font-bold mb-3">
            <a href="{file_name}" class="hover:text-[#603813]">{title}</a>
        </h2>
        <a href="{file_name}" class="text-[#603813] font-bold text-sm">সম্পূর্ণ পড়ুন →</a>
    </article>"""
            
            home_content = home_content.replace(MARKER, f"{MARKER}\n{new_card}")

    with open(HOME_PAGE, 'w', encoding='utf-8') as f:
        f.write(home_content)

if __name__ == "__main__":
    process_files()
          
