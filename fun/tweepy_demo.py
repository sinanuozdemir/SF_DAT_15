import tweepy

# PLEASE GET YOUR OWN!!!!!!!!
#  dev.twitter.com


api_key = 'Ftp4IDSOcPJaCdTlxblRMPW05'
api_secret = '6AIiTKoVC3hChn81o1pRgOlokS0sN8NsQS39TZvLyig8QE1G4k'
access_token = '3125140791-qdedGOqCFFRdvCWd7TLsVVROb2hxGuUjkfLR3R3'
access_secret = 'XeW4odbzKNB2Z8FPkmZAlWBBlbVj6cpw6tAdfBxJzOQXD'


auth = tweepy.OAuthHandler(api_key, api_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth)


tweets = tweepy.Cursor(api.search,
                           q="starbucks",
                           result_type="recent",
                           lang="en").items()

for tweet in tweets:
    print tweet.text, tweet.user.screen_name, tweet.user.friends_count