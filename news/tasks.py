import time


from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

from celery import shared_task

from django.db import IntegrityError

from news.models import News, Tag
from scraper.scrap import get_articles_data



@shared_task
def scrape_and_save_task():
    # data = subprocess.run(["python", "scrap.py"])
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--disable-gui")
    chrome_options.add_argument("--disable-extenstions")

    browser = webdriver.Chrome(options=chrome_options)
    
    browser.get("https://www.zoomit.ir/archive/")
    SCROLL_PAUSE_TIME = 2
    for _ in range(3):
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        time.sleep(SCROLL_PAUSE_TIME)

    html = browser.page_source
    soup = BeautifulSoup(html, "html.parser")

    article_divs = soup.select('div.scroll-m-16')
    links = []
    for div in article_divs:
        a_tag = div.find("a", href=True)
        if a_tag and a_tag["href"].startswith("https://www.zoomit.ir/"):
            links.append(a_tag["href"])
    
    links = list(set(links))

    data = get_articles_data(browser, links)
    
    for news in data:
        title = news['title']
        body = news['body']
        tags_name = news['tags']
        
        if News.objects.filter(title=title).exists():
            continue
        
        tags = []
        for tag_name in tags_name:
            tag, _ =  Tag.objects.get_or_create(name=tag_name)
            tags.append(tag)
            
        try:
            news = News.objects.create(title=title, body_text=body)
            news.tags.set(tags)
        except IntegrityError:
            continue