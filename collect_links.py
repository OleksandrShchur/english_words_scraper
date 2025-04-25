import requests
from bs4 import BeautifulSoup
import os

# Ensure the links folder exists
os.makedirs("links", exist_ok=True)

urls = [
    "https://langeek.co/en-UK/vocab/category/6/a2-level",
    "https://langeek.co/en-UK/vocab/category/7/b1-level",
    "https://langeek.co/en-UK/vocab/category/8/b2-level",
    "https://langeek.co/en-UK/vocab/category/35/c1-level",
    "https://langeek.co/en-UK/vocab/category/251/c2-level"
]

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
}

# Exact class string to match
target_class = "tw-text-white tw-bg-blue-1 tw-text-base tw-font-medium hover:tw-no-underline tw-py-2 tw-px-4 sm:tw-py-3 sm:tw-px-6 tw-rounded-3xl tw-flex tw-gap-1 tw-items-center tw-justify-center tw-transition-all tw-duration-300 hover:!tw-text-white hover:!tw-bg-purple"
base_url = "https://langeek.co"

for url in urls:
    file_name = url.rstrip("/").split("/")[-1].replace("-", "_")
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        response.encoding = response.apparent_encoding
        soup = BeautifulSoup(response.text, "html.parser")

        # Find all <a> tags with exact match in class attribute
        matching_links = soup.find_all("a", attrs={"class": target_class})

        hrefs = [a["href"] for a in matching_links if a.has_attr("href")]

        with open(f"links/{file_name}_links.txt", "w", encoding="utf-8") as f:
            for href in hrefs:
                f.write(f"{base_url}{href}\n")

        print(f"{len(hrefs)} matching links saved to links/{file_name}_links.txt.txt")
    else:
        print(f"Failed to retrieve page. Status code: {response.status_code}")
