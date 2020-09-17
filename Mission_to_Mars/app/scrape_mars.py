from splinter import Browser
from bs4 import BeautifulSoup as bs
import time


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
      "news_p": news_p,
   }

   # Return results
   return mars_data

   # Close the browser after scraping
   browser.quit()


def scrape_image():
   browser = init_browser()

   # Visit JPL Mars Space Images site
   url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
   browser.visit(url)

   time.sleep(1)

   # Scrape page into Soup
   html = browser.html
   soup = bs(html, "html.parser")

   # Find the src for the image
   relative_image_path = soup.select_one('figure.lede a img').get('src')
   base_url = "https://www.jpl.nasa.gov/"
   featured_image_url = base_url + relative_image_path
   featured_image_url

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

   # Return results
   return mars_data

   # Close the browser after scraping
   browser.quit()


