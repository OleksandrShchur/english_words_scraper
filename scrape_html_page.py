import requests
from bs4 import BeautifulSoup

url = "https://langeek.co/en-UK/vocab/subcategory/180/learn"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    response.encoding = response.apparent_encoding

    html_content = response.text
    soup = BeautifulSoup(html_content, "html.parser")

    with open("page.html", "w", encoding="utf-8") as f:
        f.write(soup.prettify())

    print("HTML saved and should display Ukrainian correctly.")
else:
    print(f"Failed to fetch page. Status code: {response.status_code}")
