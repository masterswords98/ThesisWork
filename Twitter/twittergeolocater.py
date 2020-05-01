
import tweepy
import pandas as pd
from csv import DictReader
from pathlib import Path
import time
import twittercredentials


with open(Path('./imyeek_followers.csv'), 'r') as read_obj:
    dict_reader = DictReader(read_obj)
    list_of_dict = list(dict_reader)
    print(list_of_dict[1])


listy = []
for i in list_of_dict:
    if int(i.get('followers_count')) < 400:
        listy.append(i.get('screen_name'))
        print(i.get('screen_name'))

print(len(listy))

# df = pd.read_csv(Path('./imyeek_followers.csv'), delimiter = ',')
# df_dicts = df.to_dict()
# print(df_dicts)

#print(df_dicts.values())
#print(df_dicts.get('screen_name'))

# if df_dicts.get('friends_count') >= 1000:
#     print(df_dicts.get('screen_name'))
    # if df_dict.get('friends_count') >= 1000:
    #     print(df_dict['screen_name'])
    # else:
    #     break


""" 
auth = tweepy.OAuthHandler(twittercredentials.CONSUMER_KEY, twittercredentials.CONSUMER_SECRET)
auth.set_access_token(twittercredentials.ACCESS_TOKEN,twittercredentials.ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

 

screennamelst = list()
namelst = list()

for u in users:   
    namelst.append(u.name)

for u in users:
    screennamelst.append(u.screen_name)

yeek_follower = pd.DataFrame({'screen_name': screennamelst, 'user_name': namelst})
yeek_follower.to_csv(r'/Users/daking/Desktop/follower_list.csv', index=False)

all_follower = list()
for i in screennamelst[0:5]:
    for u in tweepy.Cursor(api.followers, screen_name=i,count=200).items():
        all_follower.append(u.screen_name)

follower_follower_15 = pd.DataFrame({'screen_name':all_follower})
follower_follower_15.to_csv("follower's followers.csv", sep = ',')
follower_count = follower_follower_15.groupby('screen_name').size().sort_values(ascending = False)


all_friend2 = list()
for i in screennamelst[6:10]:
    for u in tweepy.Cursor(api.friends_ids, screen_name=i,count=200).items():
        all_friend2.append(u)
follower_friend610 = pd.DataFrame({'friend_id': all_friend2})
follower_friend610.to_csv("follower's friend.csv", sep = ',')


friend_count = follower_friend610.groupby('friend_id').size().sort_values(ascending = False)
friend_count2 = friend_count[friend_count>=2]

df_follower = pd.read_csv('follower.csv')
namelst = df_follower['screen_name'].tolist()

loclist = []
namelist = []
for name in namelst[1:300]:
    try:
        user_tweets = api.user_timeline(screen_name= name, count=2)
    except Exception as e:
        user_tweets = list([0])
    if type(user_tweets) == list:
        loclist.append('Private Account')
        namelist.append('Private Account')
    else:
        for tweet in user_tweets[1:2]:
            loclist.append(tweet.user.location)
            namelist.append(tweet.user.name)

df_300 = pd.DataFrame({'1. name':namelist, '2. location':loclist})
df_300.to_csv('follower_location.csv', sep=',')  
"""


