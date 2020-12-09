#!/usr/bin/env python
# coding: utf-8

# # Mission to Mars

# A web application that scrapes various websites for data related to the Mission to Mars and displays the information in a single HTML page.

# In[99]:


# Dependencies
from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
import requests
import pymongo
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
from webdriver_manager.chrome import ChromeDriverManager
import time


# In[116]:


#
#executable_path = {'executable_path': 'C:\\Users\\ericf\\OneDrive\\Desktop\chromedriver'}
#browser = Browser('chrome', **executable_path, headless=False)


# In[119]:


#news_url = "https://mars.nasa.gov/news/"
#browser.visit(url)


# In[121]:


#tml = browser.html
#news_soup = bs(html, 'html.parser')


# In[126]:





# In[128]:



# HTML Object
#html = browser.html

# Parse HTML with Beautiful Soup
#soup = bs(html, 'html.parser')


# Retrieve the latest element that contains news title and news_paragraph
#news_title = soup.find('div', class_='content_title').find('a').text
#news_p = soup.find('div', class_='article_teaser_body').text

# Display scrapped data 
#print(news_title)
#print(news_p)


# ## Step 1 - Scraping
# 
# ### Nasa Mars News
# 
#     - Scrape the Nasa Mars News Site and collect the latest news title and paragraph text
#     - Assign the text to variables that you can reference later.

# In[129]:


# Visit Nasa Mars News url
url = 'https://mars.nasa.gov/news/'
response = requests.get(url)


# In[130]:


# Parse HTML with BeautifulSoup
soup = bs(response.text, 'html.parser')


# In[131]:


print(soup.prettify())


# In[132]:


# Extract article title and paragraph text
#article = soup.find_all('div', class_='list_text')
news_title = soup.find_all('div', class_='content_title')[0].text
print(news_title)


# In[133]:


news_p = soup.find('div', class_='rollover_description_inner').text
print(news_p)


# ### JPL Mars Space Images - Featured Image
# 
#     - Visit url for JPL Featured Space Image and use splinter to navigate the site and find the image url for the current Featured Mars Image. Assign the url string to a variable called featured_image_url.

# In[134]:


# Visit JPL Featured Space Image url
image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
#browser.visit(image_url)
#time.sleep(2)
response = requests.get(image_url)
soup = bs(response.text, 'html.parser')


# In[135]:


print(soup.prettify())


# In[136]:


image = soup.find_all('a', class_='fancybox')
image


# In[137]:


feat_img = []
for img in image:
    pic = img['data-fancybox-href']
    feat_img.append(pic)
    
featured_img_url = 'hrrps://www.jpl.nasa.gov' + pic
featured_img_url


# ### Mars Facts

# In[45]:


fact_url = 'https://space-facts.com/mars/'
response = requests.get(fact_url)
fact_soup = bs(response.text, 'html.parser')


# In[46]:


print(fact_soup.prettify())


# In[47]:


fact_tables = pd.read_html(fact_url)
factsdf = fact_tables[0]
factsdf


# In[48]:


factsdf.columns = ['Stat', 'Measurement']
s = pd.Series(factsdf['Stat'])
factsdf['Stat'] = s.str.strip(':')
factsdf = factsdf.set_index('Stat')
factsdf


# In[49]:


#Generate HTML tables from df
html_table = factsdf.to_html()
html_table


# In[50]:


#Save as HTML file
factsdf.to_html('mars_facts_table.html')


# ### Mars Hemispheres

# In[146]:


# Set up broswer withj chromedriver
executable_path = {'executable_path': 'C:\\Users\\ericf\\OneDrive\\Desktop\chromedriver'}
browser = Browser('chrome', **executable_path, headless=False)


# In[147]:


hemi_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
browser.visit(hemi_url)


# In[141]:


response_hemi = requests.get(hemi_url)
hemi_soup = bs(response.text, 'html.parser')
print(hemi_soup.prettify())


# In[148]:



# HTML Object
html_hemis = browser.html

# Parse HTML with Beautiful Soup
soup = bs(html_hemis, 'html.parser')

# Retreive all items that contain mars hemispheres information
items = soup.find_all('div', class_='item')

# Create empty list for hemisphere urls 
hemis_image_urls = []

# Store the main_ul 
hemis_main_url = 'https://astrogeology.usgs.gov'

# Loop through the items previously stored
for i in items: 
    # Store title
    title = i.find('h3').text
    
    # Store link that leads to full image website
    part_img_url = i.find('a', class_='itemLink product-item')['href']
    
    # Visit the link that contains the full image website 
    browser.visit(hemis_main_url + part_img_url)
    
    # HTML Object of individual hemisphere information website 
    part_img_html = browser.html
    
    # Parse HTML with Beautiful Soup for every individual hemisphere
    soup = bs( partial_img_html, 'html.parser')
    
    # Retrieve full image source 
    img_url = hemis_main_url + soup.find('img', class_='wide-image')['src']
    
    # Append
    hemis_image_urls.append({"title" : title, "img_url" : img_url})
    
hemis_image_urls


# In[ ]:




