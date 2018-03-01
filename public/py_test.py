# this test file takes an encoded emai, decodes it, parese out order information and saves it to the database
# also changes the status of the messages db from "need to scrape" to "scraped"
#
#
#

#reload(sys);
#sys.setdefaultencoding("utf8")
import pandas as pd
import numpy as np
import praw
import operator
import pandas as pd
import pymongo
from pymongo import MongoClient
import time

#set up DB
#local
#client = MongoClient('mongodb://localhost:27017/test')
#db = client.test

#heroku
client = MongoClient('mongodb://heroku_zt5q0wf3:nl2kmh3nvs201j76if1d60f2h6@ds127883.mlab.com:27883/heroku_zt5q0wf3')
db = client['heroku_zt5q0wf3']

#set up praw
reddit = praw.Reddit(client_id='D7tXhzmCZKD1Ig',
                     client_secret='a8Cs1yp7GUakwc-Hzkd1twMRRcU',
                     user_agent='Script for top domains posted on reddit')

#create list of subreddits to include
s_list = \
['funny',
'todayilearned']

domains_sub = {}
domains = {}
domains_score = {}

for i in s_list:
    #pull in posts
    subreddit = reddit.subreddit(i)
    submissions = subreddit.top('week', limit=1000)

    for s in submissions:
        if s.domain in domains.keys():
            domains[s.domain] += 1
        else:
            domains[s.domain] = 1


    df_submissions = pd.DataFrame.from_dict(domains, orient='index').reset_index()
    df_submissions.columns = ['domain','submissions']


    #pull in score
    subreddit = reddit.subreddit(i)   #input('enter subreddit name: /r/'))
    submissions = subreddit.top('week', limit=1000)


    for s in submissions:
        if s.domain in domains_score.keys():
            #(1) works for generating total score:
            domains_score[s.domain] += s.score
        else:
            #(2)
            #works for generating total score:
            domains_score[s.domain] = s.score

    df_score = pd.DataFrame.from_dict(domains_score, orient='index').reset_index()
    df_score.columns = ['domain','score']

    #pull in subreddit
    subreddit = reddit.subreddit(i)
    submissions = subreddit.top('week', limit=1000)


    for s in submissions:
        if s.domain in domains_sub.keys():
            #(1) works for generating total score:
            domains_sub[s.domain] = s.subreddit.display_name
        else:
            #(2)
            #works for generating total score:
            domains_sub[s.domain] = s.subreddit.display_name



df_subreddit = pd.DataFrame.from_dict(domains_sub, orient='index').reset_index()
df_subreddit.columns = ['domain','subreddit']


#post processing
df_submissions_score = df_submissions.merge(df_score, how='left', on="domain")
df3 = df_submissions_score.merge(df_subreddit, how='left', on='domain')
df3 = df3.sort_values(by='submissions', ascending=0)
df3['avg_score'] = (df3.score/df3.submissions)
# Create a list to store current date
date = []
# For each row in the column,
for row in df3['domain']:
    # Append a letter grade
    date.append(time.strftime("%m/%d/%Y"))
# Create a column from the list
df3['update_date'] = date


#push to collection
for index, row in df3.iterrows():
    dic = {'domain': row['domain'],
       'submissions': row['submissions'],
       'subreddit': row['subreddit'],
       'avg_score': row['avg_score'],
       'update_date': row['update_date'],

      }
    result = db.domains.insert_one(dic)


    #this changes the status from "need to scrape" to "scraped" in
    #the messages database
    #for index, row in df.iterrows():
    #    db.messages.update_many(
    #        {"thread_id": row['thread_id']},
    #        {"$set": {"status": "scraped"}}
    #    )


    # print 'testedandsuccess'


    #print df.head()
