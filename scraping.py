# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt
from webdriver_manager.chrome import ChromeDriverManager


def scrape_all():
    # initialize browser, create data dictionary, end the web driver and return scraped data
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    news_title, news_paragraph = mars_news(browser)
    
    # run all scraping functions and store results in dictionary
    data = {
        'news_title': news_title,
        'news_paragraph': news_paragraph,
        'featured_image': featured_image(browser),
        'facts': mars_facts(),
        'last_modified': dt.datetime.now(),
        'hemispheres': mars_hemispheres(browser)
    }
    # stop webdriver and return data
    browser.quit()
    return data

### Titles and summaries
def mars_news(browser):
    # visit the mars nasa news site
    url = 'https://redplanetscience.com'
    browser.visit(url)

    # search elements with div tag and attribute list_text (i.e. <div class='list_text'>) with optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # convert browser html to soup object
    html = browser.html
    news_soup = soup(html, 'html.parser')
    # add try/except block for error handling (in case webpage format changes and breaks the script)
    try:
        slide_elem = news_soup.select_one('div.list_text')

        # Use the parent element to find the first <a> tag and save it as `news_title`
        news_title = slide_elem.find('div', class_='content_title').get_text()

        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
    except AttributeError:
        return None, None

    # return to tell python function is complete to use title and paragraph outside the function
    return news_title, news_p


### Featured Images
def featured_image(browser):
    # Visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    # find and click the full image button (second button on the page, hence index [1])
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    # add try/except for error handling
    try:
        # Find the relative image url by (1) find the img tag with class fancybox-image, then .get('src') to pull the link to the image
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
    except AttributeError:                                      # refers to invalid attribute
        return None
    # use base URL to create a complete URL
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'
    
    return img_url


### Mars facts
def mars_facts():
    try:
    # scrape the entire Mars facts table
        df = pd.read_html('https://galaxyfacts-mars.com')[0]    # pd.read_html() specifically returns a list of tables found in html, 
                                                                # by specifying [0], pandas pulls only the first table it finds and turns it into a DF
    except BaseException:                                       # BaseException is a general exception, used to catch multiple error types
        return None                                             

    # assign the column headers and set the index to be the Description column
    df.columns=['Description', 'Mars','Earth']
    df.set_index('Description', inplace=True)

    # make df html-ready for web application
    return df.to_html()


### Mars Hemisphere data
def mars_hemispheres(browser):
    # 1. Use browser to visit the URL 
    url = 'https://marshemispheres.com/'
    browser.visit(url)

    # 2. Create a list to hold the images and titles.
    hemisphere = []

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
        hemisphere.append(entry)

        #browse back
        browser.back()

    # 4. Print the list that holds the dictionary of each image url and title.
    return hemisphere

if __name__ == "__main__":
    # if running as script, print scraped data
    print(scrape_all())