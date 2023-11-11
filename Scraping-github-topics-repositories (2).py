#!/usr/bin/env python
# coding: utf-8

# ## Scraping the top repositories for Topics on GitHub
# 
#  Introduction:
#  
# - What is WebScraping?
# You may get many definations online but in simple words Web Scraping is a method to extract and retrieve information of a part of a website (or) the whole website for educational or commercial use. PLEASE NOTE THAT WEB SCRAPING CAN BE ILLEGAL IN SOME CASES AND SOME WEBSITES MAY NOT ALLOW WEBSCRAPING
# 
# - Introduction about github and the problem statement
# GitHub is a widely used platform for hosting and collaborating on software projects. This script addresses the problem of efficiently retrieving information about top repositories across diverse GitHub topics, enabling users to explore and analyze trending projects.
# 
# - The tools used for the project(Python, requests, Beautiful Soup, Pandas, Operating System)

# Here are the steps we'll follow:
# 
# 
# 1. We are going to scrape https://github.com/topics
# 2. We'll get a list of topics. For each topic, we'll get a topic title, topic page URL and topic description.
# 3. For each topic we will get top 25 repositories in the topic from the topic page
# 4. For each repository we'll grab the repo name, username, stars and repo URL
# 5. For each we'll create a CSV file in the following format:
# 
# Repo Name, Username, Stars, Repo URL three.js, mrdoob, 69700, https://github.com/mrdoop/three.js libgdx, libgdx, 18300, https://github.com/libgdx/libgdx
# 
# 

# ## Scrape the list of topics from GitHub
# 
# Explain how you'll do it
# 
# - use requests to download the page
# - use BS4 to parse and extract information
# - convert to a Pandas dataframe
# 
# Let's write a function to download the page.

# In[29]:


import requests
from bs4 import BeautifulSoup
import os
import pandas as pd
def get_topics_page():
    #TODO - add comments
    topics_url = 'https://github.com/topics'
    response = requests.get(topics_url)
    if response.status_code != 200:
        raise Exception('Failed to load page{}'.format(topic_url))
    doc = BeautifulSoup(response.text, 'html.parser')
    return doc


# - First we will import some libraries: BeautifulSoup library which help in extracting and parsing html
# - requests library to get request from the html page
# - import os to save the file in the system by providing the filepath. 

# In[30]:


doc = get_topics_page()


# In[31]:


doc.find('a')


# Let's create some helper functions to parse information the page

# In[32]:


def get_topic_titles(doc):
    selection_class = 'f3 lh-condensed mb-0 mt-1 Link--primary'
    topic_title_tags = doc.find_all('p', {'class': selection_class})
    topic_titles = []
    for tag in topic_title_tags:
        topic_titles.append(tag.text)
    return topic_titles  


# 'get_topic_titles' can be used to get the list of titles

# In[33]:


titles = get_topic_titles(doc)


# In[34]:


titles


# Similarly we have defined functions for descriptions and URLs

# In[35]:


def get_topic_descs(doc):
    desc_selector = 'f5 color-fg-muted mb-0 mt-1'
    topic_desc_tags = doc.find_all('p', {'class': desc_selector})
    topic_descs = []
    for tag in topic_desc_tags:
        topic_descs.append(tag.text.strip())  
    return topic_descs


# To get an example of the above function just run the function using print(get_topic_descs())

# In[36]:


def get_topic_urls(doc):
    topic_link_tags = doc.find_all('a', {'class': 'no-underline flex-1 d-flex flex-column'})
    topic_urls = []
    base_url = 'https://github.com'
    for tag in topic_link_tags:
        topic_urls.append(base_url + tag['href'])

    return topic_urls



# In[ ]:





# Let's put this all together into a single function

# In[37]:


def scrape_topics():
    topics_url = 'https://github.com/topics'
    response = requests.get(topics_url)
    if response.status_code != 200:
        raise Exception('Failed to load page{}'.format(topic_url))
    topics_dict = {
        'title': get_topic_titles(doc),
        'description': get_topic_descs(doc),
        'url': get_topic_urls(doc)
    }
    return pd.DataFrame(topics_dict)


# In[ ]:





# ##  Get top 25 repositories topic from a topic page
# 
# Now we can parse the html and get top 25 repositories topic from the topic page of github and then save all the files in the folder named data in csv format where each topic will have 25 repostories

# In[38]:


def get_topic_page(topic_url):
    # Download the page
    response = requests.get(topic_url)
    # Check successful response
    if response.status_code != 200:
        raise Exception('Failed to load page{}'.format(topic_url))
    # Parse using Beautiful Soup
    topic_doc = BeautifulSoup(response.text, 'html.parser')
    return topic_doc


# In[39]:


doc = get_topic_page('https://github.com/topics/3d')


# h3 tags can be obtained by inspecting the page and finding the related tags related to the topic name header. It may change in future to h1 or any other type of header tags.

# In[40]:


def get_repo_info(h3_tag, star_tag):
    #returns all the required information about the repository
    a_tags = h3_tag.find_all('a')
    username = a_tags[0].text.strip()
    repo_name = a_tags[1].text.strip()
    repo_url = base_url + a_tags[1]['href']
    stars = parse_star_count(star_tag.text.strip())
    return username, repo_name, stars, repo_url


# The above function can be run and can be checked using the print(get_repo_info())

# In[41]:


def get_topic_repos(topic_doc):
    # Get the h3 tags containing repo title, repo url and username
    h3_selection_class = 'f3 color-fg-muted text-normal lh-condensed'
    repo_tags = topic_doc.find_all('h3', {'class': h3_selection_class})
    # Get star tags
    star_tags = topic_doc.find_all('span', {'class': 'Counter js-social-count'})
    
    topic_repos_dict = {'username': [], 'repo_name': [], 'stars': [], 'repo_url': []}

    
    # Get repo info
    for i in range(len(repo_tags)):
        repo_info = get_repo_info(repo_tags[i], star_tags[i])
        topic_repos_dict['username'].append(repo_info[0])
        topic_repos_dict['repo_name'].append(repo_info[1])
        topic_repos_dict['stars'].append(repo_info[2])                                    
        topic_repos_dict['repo_url'].append(repo_info[3])    
        
    return pd.DataFrame(topic_repos_dict)


# The above function can be run and can be checked using the print(get_topic_repos())

# In[42]:


def scrape_topic(topic_url, path):
    if os.path.exists(path):
        print("The file {} already exists.Skipping...".format(path))
        return
    topic_df = get_topic_repos(get_topic_page(topic_url))
    
    topic_df.to_csv(path, index=None)


# The above function can be run and can be checked using the print(scrape_topic())

# ## Putting it all together
# 
# - We have a function to get the list of topics
# - We have a function to create CSV file for scraped repos from atopics page
# - Let's create a function to put them together

# In[43]:


def scrape_topics_repos():
    print('Scraping list of topics')
    topics_df = scrape_topics()
    
    os.makedirs('data', exist_ok=True)
    
    for index, row in topics_df.iterrows():
        scrape_topic(row['url'], 'data/{}.csv'.format(row['title']))
        print('Scraping top repositories for "{}"'.format(row['title']))


# Let's run it to scrape the top repos for all the topics on the first page of https://github.com/topics

# In[45]:


scrape_topics_repos()


# We can check that the CSVs were created properly

# In[46]:


# read and display a CSV using Pandas
df = pd.read_csv('Ajax.csv')
print(df)


# ## Referances and Future Work
# 
# - Summary:- This project was about scraping any website using basic HTML and Python skills.In this particular project I scraped https://github.com/topics to get top 25 topics and their repositories
# 
# - Referances to links that would be useful:- BeautifulSoup official document(https://www.crummy.com/software/BeautifulSoup/bs4/doc/) 
# 
# - Ideas for future work:- This is my first webscraping projectbut definetly not the last one. Future work may include exploring additional web scraping techniques, incorporating AI for repository analysis, and integrating blockchain technologies. Stay tuned for updates!
# 
# - Feel free to explore the generated CSV files in the 'data' directory for detailed information about various GitHub topics and their top repositories.

# In[ ]:





# In[ ]:




