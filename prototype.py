import os
from dotenv import load_dotenv
import requests
import praw
from bs4 import BeautifulSoup
from transformers import pipeline


#loading dotenv variables
load_dotenv()

# summarizer currently commented out to speed up testing other features
# summarizer = pipeline('summarization')


stocknames = []
stock_appearances = {}

def check_appearance(text, stockslist, appearancelist):
    for word in text.split(' '):
        for stock in stockslist:
            if word == stock or word == '$' + stock:
                if not stock in appearancelist:
                    appearancelist[stock] = 1
                else:
                    appearancelist[stock] += 1

# Scraping all stock names
source = requests.get('https://stockanalysis.com/stocks/').text
soup = BeautifulSoup(source, 'lxml')
namelist = soup.find('ul', class_='no-spacing').find_all('li')

for stockname in namelist:
    stocknames.append(stockname.a.text.split(' ')[0])


# Scraping r/wallstreetbets
reddit = praw.Reddit(
    client_id=os.getenv('CLIENT_ID'),
    client_secret=os.getenv('CLIENT_SECRET'),
    user_agent='macos:prawpractice:v1.0 (by u/kunheehadev)'
)

wallstreetbets = reddit.subreddit('wallstreetbets').hot(limit=4)

for submission in wallstreetbets:
    check_appearance(submission.title, stocknames, stock_appearances)
    print(submission.title + '\n')

print(stock_appearances)


# for submission in wallstreetbets:
#     title = summarizer(submission.title, max_length=len(
#         submission.title.split(' ')), min_length=len(submission.title.split(' ')), do_sample=False)
#     text = summarizer(submission.selftext, max_length=len(
#         submission.selftext.split(' ')), min_length=len(submission.selftext.split(' ')), do_sample=False)
#     comments = submission.comments
