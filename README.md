# Scraping the top repositories for Topics on GitHub

## Introduction:

- **What is WebScraping?**
  You may get many definitions online, but in simple words, Web Scraping is a method to extract and retrieve information from a part of a website or the whole website for educational or commercial use. PLEASE NOTE THAT WEB SCRAPING CAN BE ILLEGAL IN SOME CASES AND SOME WEBSITES MAY NOT ALLOW WEB SCRAPING.

- **Introduction about GitHub and the problem statement**
  GitHub is a widely used platform for hosting and collaborating on software projects. This script addresses the problem of efficiently retrieving information about top repositories across diverse GitHub topics, enabling users to explore and analyze trending projects.

- **The tools used for the project(Python, requests, Beautiful Soup, Pandas, Operating System)**

Here are the steps we'll follow:

1. We are going to scrape https://github.com/topics
2. We'll get a list of topics. For each topic, we'll get a topic title, topic page URL, and topic description.
3. For each topic, we will get the top 25 repositories in the topic from the topic page.


## Scrape the list of topics from GitHub

Explain how you'll do it

- use requests to download the page
- use BS4 to parse and extract information
- convert to a Pandas dataframe

Let's write a function to download the page.

```python
import requests
from bs4 import BeautifulSoup
import os
import pandas as pd

def get_topics_page():
 # TODO - add comments
 topics_url = 'https://github.com/topics'
 response = requests.get(topics_url)
 if response.status_code != 200:
     raise Exception('Failed to load page{}'.format(topic_url))
 doc = BeautifulSoup(response.text, 'html.parser')
 return doc
Scrape the list of topics from GitHub
Explain how you'll do it

use requests to download the page
use BS4 to parse and extract information
convert to a Pandas dataframe
Let's write a function to download the page.

import requests
from bs4 import BeautifulSoup
import os
import pandas as pd

def get_topics_page():
    # TODO - add comments
    topics_url = 'https://github.com/topics'
    response = requests.get(topics_url)
    if response.status_code != 200:
        raise Exception('Failed to load page{}'.format(topic_url))
    doc = BeautifulSoup(response.text, 'html.parser')
    return doc

Putting it all together
We have a function to get the list of topics
We have a function to create CSV files for scraped repos from a topics page
Let's create a function to put them together

def scrape_topics_repos():
    print('Scraping list of topics')
    topics_df = scrape_topics()

    os.makedirs('data', exist_ok=True)

    for index, row in topics_df.iterrows():
        scrape_topic(row['url'], 'data/{}.csv'.format(row['title']))
        print('Scraping top repositories for "{}"'.format(row['title']))
Let's run it to scrape the top repos for all the topics on the first page of https://github.com/topics
scrape_topics_repos()

We can check that the CSVs were created properly

# read and display a CSV using Pandas
df = pd.read_csv('Ajax.csv')
print(df)

References and Future Work
Summary:-
This project was about scraping any website using basic HTML and Python skills. In this particular project, I scraped https://github.com/topics to get the top 25 topics and their repositories.

References to links that would be useful:-
BeautifulSoup official document(https://www.crummy.com/software/BeautifulSoup/bs4/doc/)

Ideas for future work:-
This is my first web scraping project but not the last one. Future work may include exploring additional web scraping techniques, incorporating AI for repository analysis, and integrating blockchain technologies. Stay tuned for updates!

Feel free to explore the generated CSV files in the 'data' directory for detailed information about various GitHub topics and their top repositories.
