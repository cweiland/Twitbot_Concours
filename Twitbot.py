import tweepy
import yaml
import sys
import random
import time
import os


def usage() :
    print ("Usage: python Twitbot.py [argument] [nb of tweet]\n   -The first argument must be a hashtag or a keyword (trend or followback) and the second must be an int.")
    sys.exit(0)

def getapi():
    config = yaml.load(open("./token.yaml", 'r'))
    consumer_key = config["CONSUMER_KEY"]
    consumer_secret = config["CONSUMER_SECRET"]
    access_token = config["ACCESS_TOKEN"]
    access_secret = config["ACCESS_SECRET"]
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    return(tweepy.API(auth))

def follow(name) :
    if name[len(name) - 1] == ':' :
        name = name[:len(name) - 1]
    print ("Follow: " + name.encode("utf-8"))
    try : 
        api.create_friendship(name) 
        print ("Followed !")
    except Exception as ex:
        print ("Already followed ! ("+name.encode("utf-8")+")")
        print (ex)

def printTweetInfos(status) :
    print("Name : "+status._json['user']['screen_name'].encode("utf-8"))
    #print (status.full_text)
    print ("RT count : "+str(status.retweet_count))

def taff(searchRequest) :
    list_names = list()
    for status in searchRequest:
        uid = status.id
        nbRT = int(status.retweet_count);
        if "retweeted_status" in dir(status):
            tweet=status.retweeted_status.full_text
        else:
            tweet=status.full_text
        texte = tweet.split()
        
        if (nbRT > 5 and hashtag.lower() != "concours" and hashtag.lower() != "#concours") \
                or (nbRT > 1000 and (hashtag.lower() == "concours" or hashtag.lower() == "#concours")) :
            printTweetInfos(status)
            try :
                api.create_favorite(uid)
                print ("Liked !")
            except Exception as ex:
                print ("Already liked !")
                print (ex)
            try :
                api.retweet(uid)
                print ("RT !")
            except Exception as ex:
                print ("Already RT !")
                print (ex)
            print("First name : "+status._json['user']['screen_name'].encode("utf-8"))
            follow(status._json['user']['screen_name']) 
            for names in texte:
                if names and names[0] and names[0] == '@':
                    print("Names :"+names.encode("utf-8"))
                    print("Next names : "+names[1:].encode("utf-8"))
                    follow(names[1:])
        del list_names[:]
        print("################################################################")
        
        time.sleep(random.randrange(2, 10, 1))

if __name__ == "__main__":
    api = getapi()
    my_infos = api.me()
    my_id = my_infos._json['id']
    hashtag = sys.argv[1]
    if  len(sys.argv) < 2 or (len(sys.argv) < 3 and hashtag != 'followback') :
        usage()
    if hashtag == 'followback' :
        for follower in api.followers(my_id):
            follow(follower._json['screen_name'])
            print(follower._json['screen_name'])
    else :
        if hashtag == 'trend' :
            print ("Trend: " + api.trends_place(23424819)[0]['trends'][0]['query'])
            hashtag = '#' + api.trends_place(23424819)[0]['trends'][0]['query']
    if sys.argv[2].isdigit() == False :
        usage()
    searchRequest = tweepy.Cursor(api.search, q=hashtag, lang='fr', tweet_mode="extended").items(int(sys.argv[2]))
    taff(searchRequest)   
