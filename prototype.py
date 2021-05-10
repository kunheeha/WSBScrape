import praw
from transformers import pipeline
from bs4 import BeautifulSoup
import requests
summarizer = pipeline('summarization')
source = requests.get('https://stockanalysis.com/stocks/').text

soup = BeautifulSoup(source, 'lxml')
namelist = soup.find('ul', class_='no-spacing').find_all('li')

stocknames = []

for stockname in namelist:
    stocknames.append(stockname.a.text.split(' ')[0])

stock_appearances = {}


reddit = praw.Reddit(
    client_id='s6J21wKb690M-g',
    client_secret='63ZRbmPvp6aMfy2GenYBZNrHBiCckA',
    user_agent='macos:prawpractice:v1.0 (by u/kunheehadev)'
)


def check_appearance(text, stockslist, appearancelist):
    for word in text.split(' '):
        for stock in stockslist:
            if word == stock or word == '$' + stock:
                if not stock in appearancelist:
                    appearancelist[stock] = 1
                else:
                    appearancelist[stock] += 1


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
