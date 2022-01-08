#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd


# In[2]:


# set up splinter
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# In[3]:


# visit the mars nasa news site
url = 'https://redplanetscience.com'
browser.visit(url)

# search elements with div tag and attribute list_text (i.e. <div class='list_text'>) with optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)


# In[4]:


# set up html parser
html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('div.list_text')


# ### Article scraping

# In[5]:


# search slide_elem for div class='content_title', find() only searches for the first class/attribute we specify. find_all() retrieves all tags and attributes
slide_elem.find('div', class_='content_title').get_text()


# In[6]:


# store only title text in new variable
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title


# In[7]:


# same for article_teaser, this will retrieve the first article that satisfies the tag/attribute
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p


# ### Featured Images

# In[8]:


# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)


# In[9]:


# find and click the full image button (second button on the page, hence index [1])
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()


# In[10]:


# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')


# In[11]:


# Find the relative image url by (1) find the img tag with class fancybox-image, then .get('src') to pull the link to the image
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel


# In[12]:


# use base URL to create a complete URL
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url


# ### Mars facts

# In[13]:


# scrape the entire Mars facts table
df = pd.read_html('https://galaxyfacts-mars.com')[0] #pd.read_html() specifically returns a list of tables found in html, 
#by specifying [0], pandas pulls only the first table it finds and turns it into a DF

# assign the column headers and set the index to be the Description column
df.columns=['Description', 'Mars','Earth']
df.set_index('Description', inplace=True)
df


# In[14]:


# make df html-ready for web application
df.to_html()


# In[15]:


# tell splinter to quit browser
browser.quit()


# # Challenge start

# In[1]:


# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager


# In[2]:


# Set the executable path and initialize Splinter
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# ### Visit the NASA Mars News Site

# In[3]:


# Visit the mars nasa news site
url = 'https://redplanetscience.com/'
browser.visit(url)

# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)


# In[4]:


# Convert the browser html to a soup object and then quit the browser
html = browser.html
news_soup = soup(html, 'html.parser')

slide_elem = news_soup.select_one('div.list_text')


# In[5]:


slide_elem.find('div', class_='content_title')


# In[6]:


# Use the parent element to find the first a tag and save it as `news_title`
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title


# In[7]:


# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p


# ### JPL Space Images Featured Image

# In[8]:


# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)


# In[9]:


# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()


# In[10]:


# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')
img_soup


# In[11]:


# find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel


# In[12]:


# Use the base url to create an absolute url
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url


# ### Mars Facts

# In[13]:


df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.head()


# In[14]:


df.columns=['Description', 'Mars', 'Earth']
df.set_index('Description', inplace=True)
df


# In[15]:


df.to_html()


# # D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles

# ### Hemispheres

# 1. Use browser to visit the URL 
url = 'https://marshemispheres.com/'
browser.visit(url)

# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []

# 3. Write code to retrieve the image urls and titles for each hemisphere.
products = browser.find_by_css('div[class="item"] img')

# loop through each result in products
for i in range(4):
    # create dictionary
    entry = {}
    # click on thumb to get moon-specific page
    # home_page = browser.find_by_tag('img' "thumb")[0].click()
    browser.find_by_css('div[class="item"] img')[i].click()

    html = browser.html
    img_soup = soup(html, 'html.parser')

    # scrape page for img url and title
    img_url_rel = img_soup.find('a', text="Sample").get('href')
    title = img_soup.find('h2', class_="title").get_text()

    # store title and image into list from #2
    entry['img_url'] = f'{url}{img_url_rel}'
    entry["title"] = title

    # append dictionary to list
    hemisphere_image_urls.append(entry)

    #browse back
    browser.back()

# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls

# 5. Quit the browser
browser.quit()