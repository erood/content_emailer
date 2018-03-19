#important command line function to get mongo uri -- 
# heroku config --app sheltered-ocean-45405 | grep MONGODB_URI
#where you literally type in MONGODB_URI, generates code like such: mongodb://heroku_xph57032:sb1vurrej7o36g0jumoh534qpr@ds141108.mlab.com:41108/heroku_xph57032
#the code is then fed into the client
import pymongo
import pandas as pd
import pprint
import numpy as np
import csv, sys
import praw
import operator
import datetime


#set up praw
reddit = praw.Reddit(client_id='D7tXhzmCZKD1Ig',
                 client_secret='a8Cs1yp7GUakwc-Hzkd1twMRRcU',
                 user_agent='Script for top domains posted on reddit')


from pymongo import MongoClient
client = MongoClient()

client = MongoClient('mongodb://heroku_c6w3t5x5:k6orit3e4osatg7m04senkq3vn@ds163918.mlab.com:63918/heroku_c6w3t5x5')

db = client['heroku_c6w3t5x5']

users = db.users
users = pd.DataFrame(list(users.find()))
users.head()

################################################################################################

def SendEmail(to_email): 
    #gmail style docs: https://developers.google.com/gmail/design/css#example
    import smtplib  
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText

    from_address = "erood20@gmail.com"
    to_address = to_email

    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    now = datetime.datetime.now()
    subject_date = now.strftime("%m-%d-%Y")
    msg['Subject'] = "Storyrake Summary - "+subject_date
    msg['From'] = from_address
    msg['To'] = to_address

    # Create the body of the message (a plain-text and an HTML version).
    html = """\
    <html>
      <head>
        <style>
          .colored {
            font-size:16px;
          }
           .footer {
            font-size:12px;
            font-color: #777;
          }
          .reddit_table {
            border-spacing: 25px;
            font-size:16px;
            padding-left:0px;

          }

          .subreddit_row {
            font-weight:bold;
            color:#341f97;
            font-size:20px;

            }  
            .highlight{
            border: 2px solid #f99854;
            border-radius: 3px;
            padding: 4px;
            }
          .container{
            padding-left:20px;

          }
          .col-md-8{
          max-width:80%;

          }

          #body {
            font-size:16px;
          }
          #tr {

        }
        </style>
      </head>
      <div class="container">
      <body>
        <p class='colored'>Hi,<br>
        <br>
        Below is your Reddit summary:
        </p>
        """

    html +=\
    """
    <div class="col-md-8">
    <table class="reddit_table">
    """

    for index, row in df_final.iterrows():
        if index % 5 == 0:
            #html += ("<br>")
            html += (("<tr class='subreddit_row'><td><span class='highlight'>%s</span></td></tr>" %(row['subreddit'] )))

            #html += ("<thead class='row_title'><td>Link</td><td>Score</td><td>Date</td></thead>")
        else:
            pass
        html += ("<tr><td><a href=%s>%s</a></td><td>%s</td><td>%s</td></tr>" %(row['url'],row['title'], row['score']+' pts', row['time']))

    html+=\
    """
    </table>
    <hr>
    </div>

    <p class='footer'>
    <i>To add/remove subreddits, change your preferred frequency, or unsubscribe <a href=www.erikrood.com>click here</a><i>. 
    </p>
    </div>
    """

    # Record the MIME types of both parts - text/plain and text/html.
    part2 = MIMEText(html, 'html')

    # Attach parts into message container.
    # According to RFC 2046, the last part of a multipart message, in this case
    # the HTML message, is best and preferred.
    msg.attach(part2)


    # Credentials (if needed)  
    #username = 'erood20@gmail.com'  
    #password = 'uoyuktglpyvxqycv'  
    username = 'storyrake@gmail.com'
    password = 'zgatluyspdmsakag'


    # The actual mail send  
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login(username,password)  
    server.sendmail(from_address, to_address, msg.as_string())  
    server.quit()  
    

#MAIN 


for index, row in users.iterrows():
    if row['frequency'] == 'Daily':
        
        #variables
        praw_freq = 'day'
        to_email = row['email']
        s_list = row['subreddits']
        s_list = s_list.split(",")

        
        ### Crawl reddit, clean output ###
        #dictionaries
        domains_sub = {}
        domains_score = {}
        domains_title = {}
        domains_time = {}

        #loop through list of subreddits
        for i in s_list:

            #--Pull in score for given submission id--#
            subreddit = reddit.subreddit(i)   
            submissions = subreddit.top(praw_freq, limit=5)

            #sum score across submissions
            for s in submissions:
                if s.id in domains_score.keys():
                    domains_score[s.id] += s.score
                else:
                    domains_score[s.id] = s.score

            df_score = pd.DataFrame.from_dict(domains_score, orient='index').reset_index()
            df_score.columns = ['id','score']


            #--Grab subreddit for given submission ID--#
            subreddit = reddit.subreddit(i)
            submissions = subreddit.top(praw_freq, limit=5)


            for s in submissions:
                if s.id in domains_sub.keys():
                    #(1) works for generating total score:
                    domains_sub[s.id] = s.subreddit.display_name
                else:
                    #(2)
                    #works for generating total score:
                    domains_sub[s.id] = s.subreddit.display_name



            #--Grab title for given submission ID--#        
            subreddit = reddit.subreddit(i)   
            submissions = subreddit.top(praw_freq, limit=5)

            for s in submissions:
                if s.id in domains_title.keys():
                    #(1) works for generating total score:
                    domains_title[s.id] = s.title
                else:
                    #(2)
                    #works for generating total score:
                    domains_title[s.id] = s.title



            #--Grab time for given submission ID--#        
            subreddit = reddit.subreddit(i)   
            submissions = subreddit.top(praw_freq, limit=50)

            for s in submissions:
                if s.id in domains_time.keys():
                    #(1) works for generating total score:
                    domains_time[s.id] = datetime.datetime.fromtimestamp(s.created).date() #datetime.datetime.fromtimestamp(s.created)


                else:
                    #(2)
                    #works for generating total score:
                    domains_time[s.id] = datetime.datetime.fromtimestamp(s.created).date()

        df_subreddit = pd.DataFrame.from_dict(domains_sub, orient='index').reset_index()
        df_subreddit.columns = ['id','subreddit']

        df_title = pd.DataFrame.from_dict(domains_title, orient='index').reset_index()
        df_title.columns = ['id','title']

        df_time = pd.DataFrame.from_dict(domains_time, orient='index').reset_index()
        df_time.columns = ['id','time']


        #merge the three tables together, using submission ID as primary key
        df_sub_score = df_subreddit.merge(df_score, how='left', on="id")
        df_title_score_sub = df_sub_score.merge(df_title, how='left', on='id')
        df_final = df_title_score_sub.merge(df_time, how='left', on='id')


        # Add in submission URL using the 'id' 
        df_final['url'] = ['www.reddit.com/']+df_final['id'].astype(str) 

        #sort by highest score
        df_final = df_final.sort_values(['subreddit', 'score'], ascending=[True, False])

        #chop down to just subreddit, score, time, url
        df_final = df_final[['subreddit','score','time','url','title']]

        #only keep top X for given subreddit
        df_final = df_final.groupby('subreddit').head(5)
        
        #clean index to loop through 1 subreddit per 5 posts
        df_final = df_final.reset_index()
        df_final.drop(['index'], axis = 1, inplace = True)
        
        #store score as string so can label with points
        df_final['score'] = df_final['score'].astype(str)
        
        ### Send email ###
        SendEmail(to_email)
                
        
    elif row['frequency'] == 'Weekly' and datetime.datetime.today().weekday() == 3:
        
        #variables
        praw_freq = 'week'
        to_email = row['email']
        s_list = row['subreddits']
        s_list = s_list.split(",")

        
        ### Crawl reddit, clean output ###
        #dictionaries
        domains_sub = {}
        domains_score = {}
        domains_title = {}
        domains_time = {}

        #loop through list of subreddits
        for i in s_list:

            #--Pull in score for given submission id--#
            subreddit = reddit.subreddit(i)   
            submissions = subreddit.top(praw_freq, limit=5)

            #sum score across submissions
            for s in submissions:
                if s.id in domains_score.keys():
                    domains_score[s.id] += s.score
                else:
                    domains_score[s.id] = s.score

            df_score = pd.DataFrame.from_dict(domains_score, orient='index').reset_index()
            df_score.columns = ['id','score']


            #--Grab subreddit for given submission ID--#
            subreddit = reddit.subreddit(i)
            submissions = subreddit.top(praw_freq, limit=5)


            for s in submissions:
                if s.id in domains_sub.keys():
                    #(1) works for generating total score:
                    domains_sub[s.id] = s.subreddit.display_name
                else:
                    #(2)
                    #works for generating total score:
                    domains_sub[s.id] = s.subreddit.display_name



            #--Grab title for given submission ID--#        
            subreddit = reddit.subreddit(i)   
            submissions = subreddit.top(praw_freq, limit=5)

            for s in submissions:
                if s.id in domains_title.keys():
                    #(1) works for generating total score:
                    domains_title[s.id] = s.title
                else:
                    #(2)
                    #works for generating total score:
                    domains_title[s.id] = s.title



            #--Grab time for given submission ID--#        
            subreddit = reddit.subreddit(i)   
            submissions = subreddit.top(praw_freq, limit=50)

            for s in submissions:
                if s.id in domains_time.keys():
                    #(1) works for generating total score:
                    domains_time[s.id] = datetime.datetime.fromtimestamp(s.created).date() #datetime.datetime.fromtimestamp(s.created)


                else:
                    #(2)
                    #works for generating total score:
                    domains_time[s.id] = datetime.datetime.fromtimestamp(s.created).date()

        df_subreddit = pd.DataFrame.from_dict(domains_sub, orient='index').reset_index()
        df_subreddit.columns = ['id','subreddit']

        df_title = pd.DataFrame.from_dict(domains_title, orient='index').reset_index()
        df_title.columns = ['id','title']

        df_time = pd.DataFrame.from_dict(domains_time, orient='index').reset_index()
        df_time.columns = ['id','time']


        #merge the three tables together, using submission ID as primary key
        df_sub_score = df_subreddit.merge(df_score, how='left', on="id")
        df_title_score_sub = df_sub_score.merge(df_title, how='left', on='id')
        df_final = df_title_score_sub.merge(df_time, how='left', on='id')


        # Add in submission URL using the 'id' 
        df_final['url'] = ['www.reddit.com/']+df_final['id'].astype(str) 

        #sort by highest score
        df_final = df_final.sort_values(['subreddit', 'score'], ascending=[True, False])

        #chop down to just subreddit, score, time, url
        df_final = df_final[['subreddit','score','time','url','title']]

        #only keep top X for given subreddit
        df_final = df_final.groupby('subreddit').head(5)
        
        #clean index to loop through 1 subreddit per 5 posts
        df_final = df_final.reset_index()
        df_final.drop(['index'], axis = 1, inplace = True)
        
        #store score as string so can label with points
        df_final['score'] = df_final['score'].astype(str)
        
        ### Send email ###
        SendEmail(to_email)
        

    else:
        pass
