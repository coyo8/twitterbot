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

        if self.t is not None:
            return True
        else:
            return False

    def query(self):
        userList = User.query.filter_by(job_status=True).all()
        return userList

    def get_hashtag(self, user_id):
        tagList = Hashtag.query.filter_by(id=user_id).all()
        return tagList

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

    def search_and_unfav(self, username=None):
        results = self.t.favorites.list(screen_name=username, count=10, result_type='recent')

        if results:
            for r in results:
                self.t.destroy_favorite(r.id)
            print "All the recent tweets unfavorited"
        else:
            print "No tweets for unfavoriting"

    def unfavoriteTweets(self):
        userList = self.query()

        for user in userList:
            if self.get_outh(user):
                search_and_unfav(user.twitter_handle)

    def auto_rt(self, q, count=100, result_type="recent"):
        """
            Retweets tweets that match a certain phrase (hashtag, word, etc.)
        """

        result = self.search_tweets(q, count, result_type)

        for tweet in result["statuses"]:
            try:
                # don't retweet your own tweets
                if tweet["user"]["screen_name"] == TWITTER_HANDLE:
                    continue

                result = t.statuses.retweet(id=tweet["id"])
                print("retweeted: %s" % (result["text"].encode("utf-8")))

            # when you have already retweeted a tweet, this error is thrown
            except TwitterHTTPError as e:
                print("error: %s" % (str(e)))

    def auto_follow(self, q, count=100, result_type="recent"):
        """
            Follows anyone who tweets about a specific phrase (hashtag, word, etc.)
        """

        result = self.search_tweets(q, count, result_type)
        following = set(t.friends.ids(screen_name=TWITTER_HANDLE)["ids"])

        # make sure the "already followed" file exists
        if not os.path.isfile(ALREADY_FOLLOWED_FILE):
            with open(ALREADY_FOLLOWED_FILE, "w") as out_file:
                out_file.write("")

            # read in the list of user IDs that the bot has already followed in the
            # past
        do_not_follow = set()
        dnf_list = []
        with open(ALREADY_FOLLOWED_FILE) as in_file:
            for line in in_file:
                dnf_list.append(int(line))

        do_not_follow.update(set(dnf_list))
        del dnf_list

        for tweet in result["statuses"]:
            try:
                if (tweet["user"]["screen_name"] != TWITTER_HANDLE and
                        tweet["user"]["id"] not in following and
                        tweet["user"]["id"] not in do_not_follow):

                    t.friendships.create(user_id=tweet["user"]["id"], follow=True)
                    following.update(set([tweet["user"]["id"]]))

                    print("followed %s" % (tweet["user"]["screen_name"]))

            except TwitterHTTPError as e:
                print("error: %s" % (str(e)))

                # quit on error unless it's because someone blocked me
                if "blocked" not in str(e).lower():
                    quit()

    def auto_follow_followers(self):
        """
            Follows back everyone who's followed you
        """

        following = set(t.friends.ids(screen_name=TWITTER_HANDLE)["ids"])
        followers = set(t.followers.ids(screen_name=TWITTER_HANDLE)["ids"])

        not_following_back = followers - following

        for user_id in not_following_back:
            try:
                t.friendships.create(user_id=user_id, follow=True)
            except Exception as e:
                print("error: %s" % (str(e)))

    def auto_unfollow_nonfollowers(self):
        """
            Unfollows everyone who hasn't followed you back
        """

        following = set(t.friends.ids(screen_name=TWITTER_HANDLE)["ids"])
        followers = set(t.followers.ids(screen_name=TWITTER_HANDLE)["ids"])

        # put user IDs here that you want to keep following even if they don't
        # follow you back
        users_keep_following = set([])

        not_following_back = following - followers

        # make sure the "already followed" file exists
        if not os.path.isfile(ALREADY_FOLLOWED_FILE):
            with open(ALREADY_FOLLOWED_FILE, "w") as out_file:
                out_file.write("")

        # update the "already followed" file with users who didn't follow back
        already_followed = set(not_following_back)
        af_list = []
        with open(ALREADY_FOLLOWED_FILE) as in_file:
            for line in in_file:
                af_list.append(int(line))

        already_followed.update(set(af_list))
        del af_list

        with open(ALREADY_FOLLOWED_FILE, "w") as out_file:
            for val in already_followed:
                out_file.write(str(val) + "\n")

        for user_id in not_following_back:
            if user_id not in users_keep_following:
                t.friendships.destroy(user_id=user_id)
                print("unfollowed %d" % (user_id))
