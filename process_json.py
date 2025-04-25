import requests
from bs4 import BeautifulSoup
import json
import os

# Ensure the links folder exists
os.makedirs("words", exist_ok=True)

file_names = [
    "links/a2_level_links.txt",
    "links/b1_level_links.txt",
    "links/b2_level_links.txt",
    "links/c1_level_links.txt",
    "links/c2_level_links.txt"
]

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
}

def extract_word_translation(cards_raw):
    extracted = []

    for group in cards_raw:
        if isinstance(group, list):
            for card in group:
                try:
                    word = card["mainTranslation"]["title"]
                    translation = card["mainTranslation"]["localizedProperties"]["translation"]
                    extracted.append({
                        "word": word,
                        "translation": translation
                    })
                except (KeyError, TypeError):
                    continue
    return extracted

def extract_all_cards(obj, property_key):
    cards_list = []

    if isinstance(obj, dict):
        for key, value in obj.items():
            if key == property_key:
                cards_list.append(value)
            else:
                cards_list.extend(extract_all_cards(value, property_key))
    elif isinstance(obj, list):
        for item in obj:
            cards_list.extend(extract_all_cards(item, property_key))

    return cards_list

for file_name in file_names:
    with open(file_name, "r", encoding="utf-8") as file:
        urls = [line.strip() for line in file if line.strip()]

    all_words = []

    for url in urls:
        print(f"🔍 Processing: {url}")
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            response.encoding = response.apparent_encoding
            soup = BeautifulSoup(response.text, "html.parser")

            script_tag = soup.find("script", id="__NEXT_DATA__")

            if script_tag:
                try:
                    json_data = json.loads(script_tag.string)
                    cards_data = extract_all_cards(json_data, "cards")
                    words = extract_word_translation(cards_data)
                    all_words.extend(words)
                    print(f"✅ Extracted {len(words)} words")
                except Exception as e:
                    print(f"⚠️ Error parsing JSON from {url}: {e}")
            else:
                print(f"❌ No __NEXT_DATA__ found in {url}")
        else:
            print(f"❌ Failed to load {url} — Status code: {response.status_code}")

    translation_file_name = file_name.split("_")[0].split("/")[-1]
    
    with open(f"words/{translation_file_name}_words.json", "w", encoding="utf-8") as f:
        json.dump(all_words, f, ensure_ascii=False, indent=2)

    print(f"\n📦 Done! Saved {len(all_words)} words total to words/{translation_file_name}_words.json")
