import pandas as pd
from bs4 import BeautifulSoup
from splinter import Browser

def scrape():
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)

    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    news_title = soup.find(class_='content_title').find('a').text

    news_description = soup.find(class_='article_teaser_body').text

    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    img_link_inc= soup.find(class_="default floating_text_area ms-layer").find('a')['data-fancybox-href']
    img_link = "https://www.jpl.nasa.gov" + img_link_inc

    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    weather_link = soup.find(class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text').text

    url = 'http://space-facts.com/mars/'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    data_table = pd.read_html(url)

    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    hemispheres = ['Cerberus Hemisphere Enhanced','Schiaparelli Hemisphere Enhanced', 'Syrtis Major Hemisphere Enhanced', 'Valles Marineris Hemisphere Enhanced' ]
    hemisphere_photos = []

    for items in hemispheres:
        hemdict = {}
        browser.click_link_by_partial_text(items)
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        hemdict['img_url'] = soup.find(class_='downloads').find('a')['href']
        hemdict['title'] = items
        url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
        browser.visit(url)
        html = browser.html
        hemisphere_photos.append(hemdict)

    output = {'newsTitle':news_title,
            'newsDesciption':news_description,
            'jplImage': img_link,
            'weather':weather_link,
            'dataTable':data_table,
            'hemispherePhotos':hemisphere_photos }
    return output


