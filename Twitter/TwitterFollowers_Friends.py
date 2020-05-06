import time
import tweepy
import pandas as pd
from pathlib import Path
import csv
from csv import DictReader
import numpy as np
import random
import twittercredentials

auth = tweepy.OAuthHandler(twittercredentials.CONSUMER_KEY, twittercredentials.CONSUMER_SECRET)
auth.set_access_token(twittercredentials.ACCESS_TOKEN,twittercredentials.ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)


#The given Path for each of the list of followers drawn for each artist
yeek_followers = Path('./imyeek_followers.csv')
dom_followers = Path('./dominicfike_followers.csv')
bakar_followers = Path('./yeaabk_followers.csv')
omar_followers = Path('./omarapollo_followers.csv')

#Converts the information from the csv containing each artists followers into a list in Python
def followerids_to_list(direction):
    with open(direction, 'r') as read_obj:
        dict_reader = DictReader(read_obj)
        list_of_dict = list(dict_reader)
        #print(list_of_dict[1])

    listy = []
    for i in list_of_dict:
        if(int(i.get('friends_count')) <= 400): 
            listy.append(i.get('screen_name'))

    test_list = []
    for i in range(0,300):
        screen_name = np.random.choice(listy, replace=False)
        screen_name = ''+screen_name+''
        test_list.append(screen_name)
        i+=1
    #print(test_list)
    return test_list

#Returns who is following the user in question
def get_the_followers(user_name):
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

#Returns if a user has a private or a public account
def get_unprotected(ids):
    unprotected_users = []
    for user_name in ids:
        try:
            user = api.get_user(screen_name = user_name, wait_on_rate_limit = True, count =900)
            if(user.protected==False):
                unprotected_users.append(user_name)
                #print(user_name)         
        except tweepy.error.TweepError as ex:
            if(ex.api_code == 88):
                print("Going to sleep:", ex)
                time.sleep(180)
            elif(ex.api_code == 50):
                pass 
    print(unprotected_users)
    return(unprotected_users)
    
#Gets who the user from a list of users is following
def get_the_friendships(ids):

    api = tweepy.API(auth)
    final_peeps = []
    for name in ids:
        peeps = []
        for page in tweepy.Cursor(api.friends, screen_name = name, wait_on_rate_limit=True, count=200).pages():
            try:
                peeps.extend(page)
            except tweepy.TweepError as ex:
                print("Going to sleep:", ex)
                time.sleep(180)        
        final_peeps.extend(peeps)
    print(final_peeps)
    return final_peeps

#Converts the information which is returned from get_followers() about each of the artists followers from a json format
#into a csv format that can be easily exported
def save_followers_to_csv(user_name, data):
    """
    saves json data to csv
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

#Converts the information which is returned from get_friends() about each of the users followed by 
# an artists followers from a json format into a csv format that can be easily exported
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

#Subsets the list of public users within the artists' list of followers into a list each containing only 6 users
#This was done for the sake of efficiency, and so as not to exceed the rate limit 
yeek_list = ['mannyfisherman', '_jessyyyca', 'yngfabe', 'andrewrevas', 'SexauerEllie', 'jasoncmcgourty', 'violettdaze', 'graciieee23', 'joshehllers', 'jennnifer182', 'TheWaveForum', 'wormsinmymouf', 'earlrondelavega', 'calqui33', 'tiffaaannnyyy', 'samamelia_', 'StacySibri', 'myadidasrdusty', 'xandersebolt', 'jorge04786', 'YymsjyJ9T47oVXs', 'emuwutea', 'Old_Account6576', 'htxkevinnn', 'MissMcfly_', 'Barajassssss', 'hntrbrynt', 'notmygovname', 'xxxtent', 'jpalacios116', 'joychristn', 'rev_isla_mp3', 'cookies0ul', 'Cvzyboi', 'RonnyInBoxLogos', 'spookyjoys', 'LottiePolka', 'ninanerviosa', '500DaysOfSassy', 'cachenbaugh_', 'ureno_natalie', 'remyfranco_', '1_Stephens_8', 'beautiulbutches', '02kennth', 'egirlsara', 'cmzrfdl', 'Rekoverii', 'kissytracy', 'biancalaureng', 'fiwstockford', 'mattbobovecz', 'bradleysparks03', 'kikirara_101', 'IiIdoink', 'selahxconde', 'GULLYXSKULLYX', 'qhx_1', 'LokoGuillaume', 'mattsabean1', 'AlcorMizar_', 'yerisnovio', 'kushs_', 'rain_luu', 'jayagrocerer', 'xmarciana', 'a1chera_', 'isleepwitjeans', 'UngDar', 'Camilo_Yepes0', 'aijanipyne', 'gabyyxo19', 'stuartmartin201', 'MinoySun', 'danafrmartin', 'aidanabelha', 'm_gomez27', 'ddanielcarrasco', 'stephaniecera', 'ksmoore17', 'lil_titz', 'harisrazaq23', 'aanibiorka', 'lancesalcedo_', 'rev_isla_mp3', 'NickelTheKing', 'pasatin_', 'jasoncmcgourty', 'mikechiiii', 'MyronAG', 'eurekaaa123', 'crewneck1234', 'christian34554', 'ChanTheArts', 'slvrbanana', 'cruzjordan165', 'alizontra', 'AndersonAliza', 'impatrick80', 'ashdani_', '_jeanna_', 'kennethfdeleon', 'foolicooly', 'Startouf73', 'sophbug04', 'poppascelia', 'ChanTheArts', 'mjose6673', 'mrndasnchz', 'brwneyedgirl2', 'eliananashh', 'karenatapiaa', 'teendeadstar', '_simply_maddy_', 'thatoneguyjalen', 'simpgod4', 'IegaIizeranch', 'groovybex', 'kendogblaze', 'lilyolss', 'mccoy_camri', 'ataopapinto', 'StacySibri', 'christnachung', 'tanaiiaa8', 'j3mm4f1nch', '_astroian', 'j_is_4_jaz', 'fpplliya', 'esahheee', 'NikTheFuckFace', 'syris__', 'growupjessica', 'caitlinnelll', 'esther50472382', 'abrahamlearning', 'ianpiova', 'heidisnightmare', 'Mk_gee_', 'Arpanosa', 'CalvinKomape', 'mvxx98', 'DanielGlowmez', '19minphoto', 'carlos_rdgzz', 'MadeMoc', 'lilsterrs', 'celestenorum', 'trashykare13', 'ianpiova', 'easyux2', 'vnessamariev', 'GarcciaVanessa', 'JeffreyTaetsch', 'roseluvrr', 'ZoeCas159', 'shanamct', 'abrahamlearning', 'theagabrielleg', 'jessm0ral3s', 'chapstikkneeded', 'inluvwithmarie', 'hannahgg2499', 'knaghstee', 'endawns', 'tanaiiaa', 'PleeceHelpMe', 'Eflowrae1', 'tavareslucas', 'ZoeCas159', 'AlexOch79531860', 'milbourn_zach', 'oplaadsnoer', 'davdalan', 'kendrasnchz', 'LamprosJacob', 'taco3ella', 'a_revlo', 'crazyfrog_irl', 'ChockoMelk', 'yang_yang808', 'whobryantt', 'Itskevi78699664', 'obamaunni', 'crewneck1234', 'BradyyyIan', 'gloryyLOVE', 'BigdomeTyler', 'Elfallever', 'starboyclique', 'mariispooks', 'zzyyoonn', 'blonded07', 'obamaunni', 'NoahRamos8', 'gulgamorjil', 'yang_yang808', 'L0VETAP3', 'mcerda23', 'jojonasfanclub', 'kaitlynuwu', 'mannithecreator', 'biggerzestier61', 'kdtherjne', 'redheadsaam', 'natalieericson_', 'albertodxlcampo', 'miyaaaa_t', 'davidg2531', 'AndersonAliza', '_tunnelovision', 'niekbeats', 'selahxconde', 'Camilo_Yepes0', 'bettycinema', 'ickydamiann', 'rrruuddee', 'SelfishlyISink', 'MimiSmithxo', 'melisamendesz', 'papaguaam', 'scccyqqq', '40I32', 'adreunn', '02kennth', 'esme4182', 'will9w', 'grassyourself', 'danielmendeess7', 'clusellajr', 'patriciactl', '__Cadz', 'IegaIizeranch', 'Rayce21CReW', 'priscisnuggies', 'justmarwaa', 'hijodesum4dre', 'luizecirule1', 'heavensnat', 'jenlouiee', 'stolenchains', 'genya_hamada', 'ryanmurphy411', 'shitstickk', 'mikeysgnarly', 'alvarezzz_n', 'Owen__Manning', 'biggerzestier61', 'WarnackJoseph', 'Syd_lucero6', 'Hennrrryyyy', 'jjoshypoo', 'notjackhanscom', 'timdecoff', 'Karlittaaa___', 'd3adman_luzif3r', 'jonchuaa', 'negro_cowboy', 'easyux2', 'connorburg_', 'tinadoann', 'ratspeaker', 'trinitykaseyy', 'Kursh10', 'bossamocha', 'Ertpp']
yeek_list1 = yeek_list[0:6]
yeek_list2 = yeek_list[7:12]
yeek_list3 = yeek_list[13:18]
yeek_list4 = yeek_list[19:24]
yeek_list5 = yeek_list[25:32]
yeek_list6 = yeek_list[32:38]
yeek_list7 = yeek_list[39:44]
yeek_list8 = yeek_list[45:50]


#Subsets the list of public users within the artists' list of followers into a list each containing only 6 users
#This was done for the sake of efficiency, and so as not to exceed the rate limit 
dom_list = get_unprotected(followerids_to_list(Path('./dominic_followers.csv')))
dom_list1 = dom_list[0:6]
dom_list2 = dom_list[7:12]
dom_list3 = dom_list[13:18]
dom_list4 = dom_list[19:24]
dom_list5 = dom_list[25:32]
dom_list6 = dom_list[32:38]
dom_list7 = dom_list[39:44]
dom_list8 = dom_list[45:50]

#Subsets the list of public users within the artists' list of followers into a list each containing only 6 users
#This was done for the sake of efficiency, and so as not to exceed the rate limit 
bakar_list = get_unprotected(followerids_to_list(Path('./yeaabk_followers.csv')))
bakar_list1 = bakar_list[0:6]
bakar_list2 = bakar_list[7:12]
bakar_list3 = bakar_list[13:18]
bakar_list4 = bakar_list[19:24]
bakar_list5 = bakar_list[25:32]
bakar_list6 = bakar_list[32:38]
bakar_list7 = bakar_list[39:44]
bakar_list8 = bakar_list[45:50]

#Subsets the list of public users within the artists' list of followers into a list each containing only 6 users
#This was done for the sake of efficiency, and so as not to exceed the rate limit 
omar_list = get_unprotected(followerids_to_list(Path('./omarapollo_followers.csv')))
omar_list1 = omar_list[0:6]
omar_list2 = omar_list[7:12]
omar_list3 = omar_list[13:18]
omar_list4 = omar_list[19:24]
omar_list5 = omar_list[25:32]
omar_list6 = omar_list[32:38]
omar_list7 = omar_list[39:44]
omar_list8 = omar_list[45:50]


#Executes all of the functions above for the artists yeek, omar apollo, dominic fike, and bakar
if __name__ == '__main__':
    followers = get_the_followers("imyeek")
    save_followers_to_csv("imyeek", followers)
    followers2 = get_the_followers("yeaabk")
    save_followers_to_csv("yeaabk", followers2)
    followers3 = get_the_followers("dominicfike")
    save_followers_to_csv("dominic", followers3)
    followers4 = get_the_followers("omarapollo")
    save_followers_to_csv("omarapollo", followers4)
    friends_yeek = get_the_friendships(yeek_list1)
    friends_yeek.extend(get_the_friendships(yeek_list2))
    friends_yeek.extend(get_the_friendships(yeek_list3))    
    friends_yeek.extend(get_the_friendships(yeek_list4))    
    friends_yeek.extend(get_the_friendships(yeek_list5))
    friends_yeek.extend(get_the_friendships(yeek_list6))
    friends_yeek.extend(get_the_friendships(yeek_list7))
    friends_yeek.extend(get_the_friendships(yeek_list8))
    save_friends_to_csv("imyeek", friends_yeek)
    friends_dom = get_the_friendships(dom_list1)
    friends_dom.extend(get_the_friendships(dom_list2))
    friends_dom.extend(get_the_friendships(dom_list3))    
    friends_dom.extend(get_the_friendships(dom_list4))    
    friends_dom.extend(get_the_friendships(dom_list5))
    friends_dom.extend(get_the_friendships(dom_list6))
    friends_dom.extend(get_the_friendships(dom_list7))
    friends_dom.extend(get_the_friendships(dom_list8))
    save_friends_to_csv("dominicfike", friends_dom)
    friends_bakar = get_the_friendships(bakar_list1)
    friends_bakar.extend(get_the_friendships(bakar_list2))
    friends_bakar.extend(get_the_friendships(bakar_list3))    
    friends_bakar.extend(get_the_friendships(bakar_list4))    
    friends_bakar.extend(get_the_friendships(bakar_list5))
    friends_bakar.extend(get_the_friendships(bakar_list6))
    friends_bakar.extend(get_the_friendships(bakar_list7))
    friends_bakar.extend(get_the_friendships(bakar_list8))
    save_friends_to_csv("yeaabk", friends_bakar)
    friends_omar = get_the_friendships(omar_list1)
    friends_omar.extend(get_the_friendships(omar_list2))
    friends_omar.extend(get_the_friendships(omar_list3))    
    friends_omar.extend(get_the_friendships(omar_list4))    
    friends_omar.extend(get_the_friendships(omar_list5))
    friends_omar.extend(get_the_friendships(omar_list6))
    friends_omar.extend(get_the_friendships(omar_list7))
    friends_omar.extend(get_the_friendships(omar_list8))
    save_friends_to_csv("apollo", friends_omar)