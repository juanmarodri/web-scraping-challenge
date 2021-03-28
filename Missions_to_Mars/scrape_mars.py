from bs4 import BeautifulSoup as soup
import requests
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import pymongo


def scrape():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(url)
    html = browser.html
    soup_news = soup(html, 'html.parser')
    list_first = soup_news.find('li', class_ = 'slide')
    news_title = list_first.find('div', class_= 'content_title').text
    news_p = list_first.find('div', class_ = 'article_teaser_body').text

    url2 = 'https://www.jpl.nasa.gov/images?search=&category=Mars'
    browser.visit(url2)
    html = browser.html
    soup_jpl = soup(html, 'html.parser')
    featured_image_url = soup_jpl.find('div', class_ = 'BaseImage  object-contain')

    url3 = 'https://space-facts.com/mars/'
    tables = pd.read_html(url3)
    planet_facts_table = tables[1]

    url4 = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url4)
    image_urls = []
    links = browser.find_by_css('a.product-item img')
    for j in range(len(links)):
        hemisphere = {}
        
        browser.find_by_css('a.product-item img')[j].click()
        
        sample = browser.links.find_by_text('Sample').first
        hemisphere['image_url'] = sample['href']
        
        hemisphere['title'] = browser.find_by_css('h2.title').text
        
        image_urls.append(hemisphere)
        
        browser.back()
    

    mars_data = {
        'news_title': news_title,
        'news_p': news_p,
        'featured_image_url': featured_image_url,
        'planet_facts_table': planet_facts_table,
        'image_urls' : image_urls
    }

    browser.quit()

    return mars_data