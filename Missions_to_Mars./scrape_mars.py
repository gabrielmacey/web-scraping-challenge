from bs4 import BeautifulSoup as bs
import requests
from splinter import Browser
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager

def scrape():
    # URL to be scraped
    url = 'https://mars.nasa.gov/news/'
    response = requests.get(url)

    # Create BeautifulSoup object; parse with 'html.parser'
    soup = bs(response.text, 'html.parser')
    results = soup.find_all('div', class_="content_title")[0].text
    newstitles_cleaned = results.strip('\n\n')

    #Find paragraph below title
    paragraphs = soup.find_all('div', class_="rollover_description_inner")[0].text
    nparagraph = paragraphs.strip('\n\n')

    # JPL Mars Space Images
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    iurl = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(iurl)

    response = requests.get(url)
    soup = bs(response.text, 'html.parser')

    # Setting up windows browser with chromedriver
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    nasa_url = 'https://www.jpl.nasa.gov'
    images_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(images_url)
    html = browser.html
    images_soup = bs(html, 'html.parser')

    # Retrieve featured image link
    featured_image  = images_soup.find('article', class_="carousel_item")['style'].replace('background-image: url(','').replace(');', '')[1:-1]
    featured_image_url = nasa_url + featured_image

    # Mars Facts
    facts_url = 'https://space-facts.com/mars/'
    response = requests.get(facts_url)
    facts_soup = bs(response.text, 'html.parser')

    table = pd.read_html(facts_url)
    mars_table = table[0]
    facts = mars_table.rename(columns={0 : "Attribute", 1 : "Value"})
    mars_table = facts.to_html()

    # Setting up windows browser with chromedriver
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    hemi_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemi_url)
    mars_hemi_html = browser.html
    mars_soup = bs(mars_hemi_html, 'html.parser')
    mars_hemi = mars_soup.find('div', class_='collapsible results')
    mars_hemispheres = mars_hemi.find_all('a')


    hemispheres_images = []
    for x in mars_hemispheres:
        if x.h3:
            i_title = x.h3.text
            i_link = x["href"]
            base_url = "https://astrogeology.usgs.gov/"
            next_url = base_url + i_link
            browser.visit(next_url)
            i_html = browser.html
            i_soup = bs(i_html, 'html.parser')
            hemi = i_soup.find("div",class_= "downloads")
            i_image = hemi.ul.a["href"]
            mars_dict = {}
            mars_dict["Title"] = i_title
            mars_dict["Image_URL"] = i_image
            hemispheres_images.append(mars_dict)
            browser.back()

    # Putting info into dict
    mars = {
    'newstitles_cleaned': newstitles_cleaned,
    'nparagraph': nparagraph,
    'featured_image_url' : featured_image_url,
    'mars_table': mars_table,
    'hemispheres_images': hemispheres_images
    }

    return mars
