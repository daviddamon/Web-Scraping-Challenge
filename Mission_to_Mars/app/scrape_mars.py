from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
import pandas as pd


def init_browser():
   executable_path = {"executable_path": 'C:/Users/dave/chromedriver_win32/chromedriver.exe'}
   return Browser("chrome", **executable_path, headless=False)

# Create empty master dictionary 
mars_data = {}


def scrape_news():
   browser = init_browser()

   # Visit NASA Mars News Site
   url = "https://mars.nasa.gov/news/"
   browser.visit(url)

   time.sleep(1)

   # Scrape page into Soup
   html = browser.html
   soup = bs(html, "html.parser")

   # Get the news title
   news_title = soup.find('div', class_='content_title')

   # Get the news paragraph
   news_p = soup.find('div', class_='article_teaser_body')

   # Store data in master dictionary
   mars_data = {
      "news_title": news_title,
      "news_p": news_p
   }

   # Close the browser after scraping
   browser.quit()

   # Return results
   return mars_data


def scrape_image():
   browser = init_browser()

   # Visit JPL Mars Space Images site
   base_url = "https://www.jpl.nasa.gov/"
   url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
   browser.visit(url)

   time.sleep(1)

   # Scrape page into Soup
   html = browser.html
   soup = bs(html, "html.parser")

   # Find the src for the image
   relative_image_path = soup.select_one('figure.lede a img').get('src')
   featured_image_url = base_url + relative_image_path

   # Store data in master dictionary
   mars_data["featured_image_url"] = featured_image_url

   # Close the browser after scraping
   browser.quit()

   # Return results
   return mars_data

   
def scrape_facts():
   browser = init_browser()

   # Visit Mars Facts Site
   url = "https://space-facts.com/mars/"
   browser.visit(url)

   time.sleep(1)

   # Parse web page
   tables = pd.read_html(url)
     
   facts_df = tables[0]
   facts_df.columns = ['Description', 'Value']

   html_table = facts_df.to_html(index=False)

   # Store data in master dictionary
   mars_data["html_table"] = html_table

   # Close the browser after scraping
   browser.quit()

   # Return results
   return mars_data


def scrape_hemisphere():
   browser = init_browser()

   # Visit USGS Astrogeology site
   base_url = 'https://astrogeology.usgs.gov/'
   url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
   browser.visit(url)

   time.sleep(1)

   # Scrape page into Soup
   html = browser.html
   soup = bs(html, 'html.parser')

   # Retrieve all 'items' that contain image information
   results = soup.find_all('div', class_='item')

   # Iterate through each item
   for result in results:   
      
      # get hemisphere name
      title = result.find('h3').text
      title = title.replace(" Enhanced", "")
      
      # get relative link to full image webpage
      rel_url = result.find('a', class_='itemLink product-item')['href']
      
      # concat full url and go to webpage
      browser.visit(base_url + rel_url)
      
      # get image url
      img_url = browser.find_by_text('Original')['href']

      # store data in master dictionary
      mars_data = {
         "title": title,
         "img_url": img_url
      }
      
      # Close the browser after scraping
      browser.quit()
      
      # Return results
      return mars_data


