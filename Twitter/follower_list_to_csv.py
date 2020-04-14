import tweepy
from tweepy import OAuthHandler

import numpy as np
import twittercredentials
import csv
import os


auth = OAuthHandler(twittercredentials.CONSUMER_KEY, twittercredentials.CONSUMER_SECRET)
auth.set_access_token(twittercredentials.ACCESS_TOKEN, twittercredentials.ACCESS_TOKEN_SECRET)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, compression=True)

def save_followers_status(filename,foloowersid):
    path='//content//drive//My Drive//Colab Notebooks//twitter//'+filename
    if not (os.path.isfile(path+'_followers_status.csv')):
      with open(path+'_followers_status.csv', 'wb') as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',')


    if len(foloowersid)>0:
        print("save followers status of ", filename)
        file = path + '_followers_status.csv'
        # https: // stackoverflow.com / questions / 3348460 / csv - file - written -with-python - has - blank - lines - between - each - row
        with open(file, mode='a', newline='') as csv_file:
            writer = csv.writer(csv_file, delimiter=',')
            for row in foloowersid:
                writer.writerow(np.array(row))
            csv_file.closed

def get_followers_id(person):
    foloowersid = []
    count=0

    influencer= api.get_user( screen_name=person)
    influencer_id=influencer.id
    number_of_followers=influencer.followers_count
    print("number of followers count : ",number_of_followers,'\n','user id : ',influencer_id)
    status = tweepy.Cursor(api.followers_ids, screen_name=person, tweet_mode="extended").items()
    for i in range(0,number_of_followers):
        try:
            user=next(status)
            foloowersid.append([user])
            count += 1
        except tweepy.TweepError:
            print('error limite of twiter sleep for 15 min')
            timestamp = time.strftime("%d.%m.%Y %H:%M:%S", time.localtime())
            print(timestamp)
            if len(foloowersid)>0 :
                print('the number get until this time :', count,'all folloers count is : ',number_of_followers)
                foloowersid = np.array(str(foloowersid))
                save_followers_status(person, foloowersid)
                foloowersid = []
            time.sleep(15*60)
            next(status)
        except :
            print('end of foloowers ', count, 'all followers count is : ', number_of_followers)
            foloowersid = np.array(str(foloowersid))
            save_followers_status(person, foloowersid)      
            foloowersid = []
    save_followers_status(person, foloowersid)
    # foloowersid = np.array(map(str,foloowersid))
    return foloowersid