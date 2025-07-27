from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

import time
import json

browser = webdriver.Chrome()

browser.get("https://www.zoomit.ir/archive/")


SCROLL_PAUSE_TIME = 2
last_height = browser.execute_script("return document.body.scrollHeight")

for i in range(5):
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight)")
    time.sleep(SCROLL_PAUSE_TIME)
    

html = browser.page_source
soup = BeautifulSoup(html, "html.parser")

article_divs = soup.select('div.scroll-m-16')
a_tags = soup.select("a.fNLyDV")

links = []

for div in article_divs:
    a_tag = div.find("a", href=True)
    if a_tag and a_tag["href"].startswith("https://www.zoomit.ir/"):
        links.append(a_tag["href"])

                
links = list(set(links))


def extract_tags(driver):
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    
    main = soup.find('main')
    if not main:
        return []
    
    # پیدا کردن header یا بخشی که تگ‌ها داخلش هستن
    possible_headers = main.find_all('div', recursive=True)
    tags = []

    for section in possible_headers:
        links = section.find_all('a')
        if 1 < len(links) < 10:  # چون معمولاً تعداد تگ‌ها محدوده
            tag_texts = []
            for link in links:
                span = link.find('span')
                if span and span.text.strip():
                    tag_texts.append(span.text.strip())
            if tag_texts:
                tags = tag_texts
                break
    
    return tags[:-1]

def extract_article_data(driver, url):
    driver.get(url)
    time.sleep(2)

    soup = BeautifulSoup(driver.page_source, "html.parser")

    # title
    title_elem = soup.find("h1")
    title = title_elem.get_text(strip=True) if title_elem else ""

    # body
    # article = soup.find("article")
    paragraphs = soup.find_all('span', attrs={"variant": "body"})
    body = "\n".join(p.get_text(strip=True) for p in paragraphs)

    # tags
    # tag_links = soup.select("a[href^='/tag/']")
    tags = extract_tags(driver)
    

    return {
        "title": title,
        "body": body,
        "tags": tags
    }
    
    
    
# for link in links:
#     print(extract_article_data(browser, link))
# print(extract_article_data(browser, "https://www.zoomit.ir/space/444747-elon-musk-possibility-spacex-starship-failure/"))

def dump_article_extraction(driver, links):
    # data = [extract_article_data(driver, link) for link in links]
    data = extract_article_data(driver, links)

    # چاپ امن
    for article in data:
        for k, v in article.items():
            print(f"\n=== {k.upper()} ===")
            print(v[:300] + '...' if isinstance(v, str) and len(v) > 300 else v)

    # ذخیره در فایل
    with open("article_data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        
        
# test_article_extraction(browser, "https://www.zoomit.ir/space/444747-elon-musk-possibility-spacex-starship-failure/")
dump_article_extraction(browser, "https://www.zoomit.ir/space/444791-south-korea-builds-moon-base/")