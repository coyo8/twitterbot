from twitter import *
from application.models import User, Hashtag
import sys

class TwitterFav():
    def __init__(self):
        self.t = None

    def get_outh(self, user):
        OAUTH_TOKEN = user.auth_token
        OAUTH_SECRET = user.auth_secret
        CONSUMER_KEY = user.consumer_key
        CONSUMER_SECRET = user.consumer_secret

        #print OAUTH_SECRET, OAUTH_TOKEN

        self.t = Twitter(auth=OAuth(OAUTH_TOKEN, OAUTH_SECRET, CONSUMER_KEY, CONSUMER_SECRET))

        if self.t != None:
            return True
        else:
            return False

    def query(self):
        userList = User.query.filter_by(job_status=True).all()
        return userList

    def get_hashtag(self, user_id):
        tagList = Hashtag.query.filter_by(id=user_id).all()
        return tagList

    def job_stat(self, user_id):
        user = User.query.filter_by(id=user_id).first()

    def favoriteTweets(self):
        userList = self.query()

        for user in userList:
            if self.get_outh(user):
                tagList = self.get_hashtag(user.id)
                if len(tagList) < 19:
                    for tag in tagList:
                        self.search_and_fav(tag.tag, 10)

    def search_tweets(self, q, count=100, max_id=None):
    	return self.t.search.tweets(q=q, result_type='recent', count=count, lang="en", max_id=max_id)

    def favorites_create(self, tweet):
        try:
            result = self.t.favorites.create(_id=tweet['id'])
            print "Favorited"
            return result
        except TwitterHTTPError as e:
            print "Error: ", e
            return None


    def search_and_fav(self, q, count=100, max_id=None):
        result = self.search_tweets(q, count, max_id)
        first_id = result['statuses'][0]['id']
        last_id = result['statuses'][-1]['id']
        success = 0
        for tweet in result['statuses']:
            if self.favorites_create(tweet) is not None:
                success += 1

        print "Favorited total: %i of %i" % (success, len(result['statuses']))
        print "First id %s last id %s" % (first_id, last_id)