#Import Dependencies
from bs4 import BeautifulSoup
from splinter import Browser
import pandas as pd
import requests

#Declare executable path to driver
executable_path = {'executable_path': '/users/public/chromedriver_win32/chromedriver'}
#Initialize browser with splinter
browser = Browser('chrome', **executable_path, headless=False)

#Use splinter to visit mars.nava.gov/news
url = 'https://mars.nasa.gov/news/'
browser.visit(url)

#Create object of splinter.html which will be passed into BeautifulSoup to parse the html
html = browser.html
soup_parse = BeautifulSoup(html, 'html.parser')

#Use find method to grab elements that contain titles and paragraphs
title = soup_parse.find('div', class_='content_title').text
paragraph = soup_parse.find('div', class_='article_teaser_body').text

#Print title and paragraph
print(title)
print(paragraph)

# Use splinter to go to webpage where space images are located
browser.visit('https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars')

#Beautiful Soup to parse html
soup_image = BeautifulSoup(browser.html, 'html.parser')

# Create URL string to grab image 
featured_image_url  = 'https://www.jpl.nasa.gov' + soup_image.find('article')['style'].replace('background-image: url(','').replace(');', '')[1:-1]

# Show full size image url
featured_image_url

#Go to twitter to find Mars weather
browser.visit('https://twitter.com/marswxreport?lang=en')

#Use BeautifulSoup to parse the HTML
tweet = BeautifulSoup(browser.html, 'html.parser')

#Scrape
weather_tweet = tweet.find('p', class_='TweetTextSize').text


#Read html using pandas
fact_table = pd.read_html('https://space-facts.com/mars/')

#Grab the mars fact table
mars_df = fact_table[1]

#Set names of columns
mars_df.columns = ['Planet Info', 'Mars']


#Convert DataFrame into a HTML string
mars_df.to_html()

#Use splinter to visit the webpage
browser.visit('https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars')

#Use BeautifulSoup to parse the page's html
hemisphere = BeautifulSoup(browser.html, 'html.parser')

#Grab hemisphere info
hemis_info = hemisphere.find_all('div', class_='item')

#Create empty list to hold urls
hemis_img_url = []

#set the url
url = 'https://astrogeology.usgs.gov'

#Iterate through information
for i in hemis_info:
    #Find title
    hemi_title = i.find('h3').text
    
    #Generate url path
    path = i.find('a', class_='itemLink product-item')['href']
    
    #Go to image url
    browser.visit(url + path)
    
    #BeautifulSoup to parse html
    hemi_soup = BeautifulSoup(browser.html, 'html.parser')
    
    #Place data in dictionary
    image_url = url + hemi_soup.find('img', class_='wide-image')['src']
    
    #Append the dictionary to the hemsi_img_url list
    hemis_img_url.append({"title" : title, "image_url": image_url})


            