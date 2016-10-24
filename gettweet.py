#Import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json
from HTMLParser import HTMLParser
from pyes import *
from dateutil import parser

#Variables that contains the user credentials to access Twitter API
access_token='########################################'
access_token_secret='########################################'
consumer_key='########################################'
consumer_secret='########################################'



#This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):

    def on_data(self, data):
        global conn
        #a = json.loads(HTMLParser().unescape(data))
        a = json.loads(data)
        geo = a.get('coordinates')
        if geo:
        	timestamp = parser.parse(a['created_at'])
        	timestamp = timestamp.strftime('%Y-%m-%dT%H:%M:%SZ')
        	geo = geo['coordinates']
        	conn.index({'geo':a['coordinates']['coordinates'] ,'text':a['text'],'user':a['user']['screen_name'],'time':timestamp},'twitmap', 'test-type')
        

    def on_error(self, status):
        print status


if __name__ == '__main__':

    #This handles Twitter authetification and the connection to Twitter Streaming API
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)
    conn = ES('your elasticsearch endpoint')
    try:  
        conn.indices.delete_index("twitmap")
    except:
        pass
    conn.indices.create_index("twitmap")
    mapping={"user":{"type": "string","index": "not_analyzed"},"time":{"type": "date"},"text":{"type": "string"},"geo":{"type": "geo_point"}}

    # mapping={'longitude':{'store':'yes','type':'float'},'latitude':{'store':'yes','type':'float'},'message':{'store':'yes','type':'string'}}
    conn.indices.put_mapping("test-type",{'properties':mapping}, ["twitmap"])

    #This line filter Twitter Streams to capture data by the keywords: 'python', 'javascript', 'ruby'
    GEOBOX_WORLD = [-180,-90,180,90]
    stream.filter(locations=GEOBOX_WORLD)



