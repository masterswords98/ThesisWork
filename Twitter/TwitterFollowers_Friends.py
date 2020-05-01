import time
import tweepy
import pandas as pd
from pathlib import Path
import csv
from csv import DictReader
import random
import twittercredentials

auth = tweepy.OAuthHandler(twittercredentials.CONSUMER_KEY, twittercredentials.CONSUMER_SECRET)
auth.set_access_token(twittercredentials.ACCESS_TOKEN,twittercredentials.ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

yeek_followers = Path('./imyeek_followers.csv')
dom_followers = Path('./dominicfike_followers.csv')
bakar_followers = Path('./yeaabk_followers.csv')
omar_followers = Path('./omarapollo_followers.csv')


with open(Path('./omarapollo_followers.csv'), 'r') as read_obj:
    dict_reader = DictReader(read_obj)
    list_of_dict = list(dict_reader)
    #print(list_of_dict[1])

listy = []
for i in list_of_dict:
    if int(i.get('followers_count')) < 400 and int(i.get('friends_count')) < 400: 
        listy.append(i.get('screen_name'))

test_list = []
for i in range(0,50):
    screen_name = random.choice(listy)
    screen_name = ''+screen_name+''
    test_list.append(screen_name)


def get_followers(user_name):
    """
    get a list of all followers of a twitter account
    :param user_name: twitter username without '@' symbol
    :return: list of usernames without '@' symbol
    """
    api = tweepy.API(auth)
    followers = []
    for page in tweepy.Cursor(api.followers, screen_name=user_name, wait_on_rate_limit=True,count=200).pages():
        try:
            followers.extend(page)
        except tweepy.TweepError as e:
            print("Going to sleep:", e)
            time.sleep(60)
    return followers
    
def get_friendships(ids):
    api = tweepy.API(auth)
    friends = []
    final_friends = []
    for user_name in ids:
        user = api.get_user(screen_name = user_name, wait_on_rate_limit = True)
        if(user.protected==True):
            continue
        
        for page in tweepy.Cursor(api.friends, screen_name = user_name, wait_on_rate_limit=True, count=200).pages():
            try:
                friends.extend(page)
            except tweepy.TweepError as ex:
                print("Going to sleep:", ex)
                time.sleep(60) 
        final_friends.extend(friends)
    return final_friends
    

def save_followers_to_csv(user_name, data):
    """
    saves json data to csv
    :param data: data recieved from twitter
    :return: None
    """
    HEADERS = ["name", "screen_name", "description", "followers_count", "followers_count",
               'friends_count', "listed_count", "favourites_count", "created_at", "location", ]
    with open(user_name + "_followers.csv", 'w',encoding="utf-8") as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(HEADERS)
        for profile_data in data:
            profile = []
            for header in HEADERS:
                profile.append(profile_data._json[header])
            csv_writer.writerow(profile)


def save_friends_to_csv(artist_name, data):
    HEADERS = ["name", "screen_name", "description", "followers_count", "followers_count",
                'friends_count', "listed_count", "favourites_count", "created_at", "location",]
    with open(artist_name + "_friends.csv", 'w',encoding="utf-8") as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(HEADERS)
        for profile_data in data:
            profile = []
            for header in HEADERS:
                profile.append(profile_data._json[header])
            csv_writer.writerow(profile)




if __name__ == '__main__':
    #followers = get_followers("imyeek")
    #save_followers_to_csv("imyeek", followers)
    #followers2 = get_followers("yeaabk")
    #save_followers_to_csv("yeaabk", followers2)
    #followers3 = get_followers("dominicfike")
    #followers4 = get_followers("omarapollo")
    #save_followers_to_csv("omarapollo", followers4)
    #yeek_list = csv_to_list(yeek_followers)
    #friends_yeek = get_friendships(yeek_list)
    #save_friends_to_csv("imyeek3", friends_yeek)
    #friends_dom = get_friendships(test_list)
    #save_friends_to_csv("dominicfike", friends_dom)
    #friends_bakar = get_friendships(test_list)
    #save_friends_to_csv("yeaabk", friends_bakar)
    friends_omar = get_friendships(test_list)
    save_friends_to_csv = ("omarapollo", friends_omar)