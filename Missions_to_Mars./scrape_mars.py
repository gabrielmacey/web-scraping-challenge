from bs4 import BeautifulSoup as bs
import requests
from splinter import Browser
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager

def scraped_planet():
    # URL to be scraped
    url = 'https://mars.nasa.gov/news/'
    response = requests.get(url)

    # Create BeautifulSoup object; parse with 'html.parser'
    soup = bs(response.text, 'html.parser')
    results = soup.find_all('div', class_="content_title")

    # Blank list
    news_titles = []
    # Loop over elements
    for result in results:
        if (result.a):
            if (result.a.text):
                news_titles.append(result)

    newstitles_cleaned = []
    # Print only headlines for first 5
    for x in range(5):
        var=news_titles[x].text
        newvar = var.strip('\n\n')
        newstitles_cleaned.append(newvar)

    #Find paragraph below title
    paragraphs = soup.find_all('div', class_="rollover_description_inner")

    nparagraph = []
    # Print only paragraphs for first 5
    for x in range(5):
        var=paragraphs[x].text
        newvar = var.strip('\n\n')
        nparagraph.append(newvar)

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

    jpl_nasa_url = 'https://www.jpl.nasa.gov'
    images_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(images_url)
    html = browser.html
    images_soup = bs(html, 'html.parser')

    # Retrieve featured image link
    relative_image = images_soup.find_all('img')[3]["src"]
    featured_image_url = jpl_nasa_url + relative_image

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
    mars_hemi = mars_soup.find('div', class_='collapsible results')
    mars_hemispheres = mars_hemi.find_all('a')


    imgs_url = []
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
            imgs_url.append(mars_dict)
            browser.back()

    # Putting info into dict
    planet_mars = {}
    planet_mars['news_titles'] = news_titles
    planet_mars['news_paragraph'] = news_paragraph
    planet_mars['fimage'] = relative_image
    planet_mars['mars_table'] = mars_table
    planet_mars['hemispheres_images'] = imgs_url

    browser.quit()

    return planet_mars

if __name__ == "__main__":
    scraped_planet()