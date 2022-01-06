#!/usr/bin/env python
# coding: utf-8

# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

# set up splinter
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)

# visit the mars nasa news site
url = 'https://redplanetscience.com'
browser.visit(url)

# search elements with div tag and attribute list_text (i.e. <div class='list_text'>) with optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)

# set up html parser
html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('div.list_text')


### Article scraping

# search slide_elem for div class='content_title', find() only searches for the first class/attribute we specify. find_all() retrieves all tags and attributes
slide_elem.find('div', class_='content_title').get_text()

# store only title text in new variable
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title

# same for article_teaser, this will retrieve the first article that satisfies the tag/attribute
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p


### Featured Images

# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)

# find and click the full image button (second button on the page, hence index [1])
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()

# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')

# Find the relative image url by (1) find the img tag with class fancybox-image, then .get('src') to pull the link to the image
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel

# use base URL to create a complete URL
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url


### Mars facts

# scrape the entire Mars facts table
df = pd.read_html('https://galaxyfacts-mars.com')[0] #pd.read_html() specifically returns a list of tables found in html, 
#by specifying [0], pandas pulls only the first table it finds and turns it into a DF

# assign the column headers and set the index to be the Description column
df.columns=['Description', 'Mars','Earth']
df.set_index('Description', inplace=True)
df

# make df html-ready for web application
df.to_html()

# tell splinter to quit browser
browser.quit()

