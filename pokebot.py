import tweepy
import time
import os
import random

token= os.getenv('TOKEN')
token_secret= os.getenv('TOKEN_SECRET')
consumer_key= os.getenv('CONSUMER_KEY')
consumer_secret=os.getenv('CONSUMER_SECRET')

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(token, token_secret)

api = tweepy.API(auth,wait_on_rate_limit=True)

def readlastseen(fname):
    fread=open(fname,'r')
    lastseen=int(fread.read().strip())
    fread.close()
    return lastseen

def storelastseen(fname,content):
    fwrite=open(fname,'w')
    fwrite.write(str(content))
    fwrite.close()

def reply():
    lastseen=readlastseen('lastseen.txt')
    mentions=api.mentions_timeline(lastseen,tweet_mode='extended')
    for m in reversed(mentions):
        if not m:
            return
        print(str(m.id) + ' - ' + m.full_text)
        lastseen=m.id
        storelastseen('lastseen.txt',lastseen)
        text=m.full_text.lower()
        if('adopt a pokemon' in text or 'adopt a pokémon' in text):
            api.update_with_media(filename='./pokemon_jpg/'+str(random.randint(1,794))+'.jpg',status='@'+m.user.screen_name+' Hey, here is your pokemon pet!',in_reply_to_status_id=m.id)
        elif('are you ready' in text and m.user.screen_name=='zotako01'):
            api.update_with_media(filename='aye.png',status='@'+m.user.screen_name+' o7',in_reply_to_status_id=m.id)
while True:
    try:
        reply()
    except tweepy.RateLimitError:
        time.sleep(15*60)
