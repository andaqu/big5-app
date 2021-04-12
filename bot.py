from requests.exceptions import ChunkedEncodingError
import tweepy as tw
import os
import re

REQUEST_LIMIT = 200

class Tweety:

    def __init__(self, tweets_to_extract:int):
        
        # `tweets_to_extract` is the total number of tweets to extract from every user
        self.tweets_to_extract = tweets_to_extract

        # create OAuth instance
        auth = tw.OAuthHandler(os.environ.get("CONSUMER_KEY"), os.environ.get("CONSUMER_SECRET"))
        auth.set_access_token(os.environ.get("ACCESS_KEY"), os.environ.get("ACCESS_SECRET"))

        self.API = tw.API(auth, wait_on_rate_limit = True, wait_on_rate_limit_notify = True)

    def textualise(self, tweets):
        
        # Join tweet text to a single string
        document = " ".join([t.full_text for t in tweets])

        # Lowercase document
        document = document.lower()

        # Remove usernames
        document = re.sub(r"@[^\s]+", "", document)

        # Remove URLs
        document = re.sub(r"(http|www)\S+", "", document)

        # Replace with ’ with '
        document = re.sub("’", "'", document)

        # Replace non-latin letters with a space
        document = re.sub(r"[^A-Za-z'\-]", " ", document)

        # Remove any apostrophes or dashes not within two letters
        document = re.sub(r"(?<!\w)(\'|\-)|(\'|\-)(?!\w)", "", document)

        # Convert multiple spaces to a single space
        document = " ".join(document.split())

        return document

    def get_document(self, user_id:str, stored_tweets:int = 0, first:int = None, last:int = None):
        """
        If tweets of user with user_id have already been extracted, the total number of stored tweets, the first tweet id and the last tweet id are to be specified. The function checks if new tweets have been posted, and if not, it continues where it left off; else it starts over.

        Returns False if the user account is invalid or what is stored is greater than what is to be extracted.
        Else, it returns the pre-processed text from the tweets of the user with the specified user_id. It also returns the first and last tweet ids to update within the database, alongside the current total of tweets, which is to be accumulated with the database's total.
        """
        
        #* 3-input XOR ( ͡° ͜ʖ ͡°)
        if (bool(stored_tweets) ^ bool(first)) | (bool(first) ^ bool(last)):
            return {"valid": False, "output": f"User [{user_id}]: stored_tweets, first, and last parameters must either all be specified or omitted altogether.", "sleep": False}

        extracted_tweets = []
        tweets_to_extract = self.tweets_to_extract

        # Retrieve the first tweet to check if user exists
        try:
            first_tweet = self.API.user_timeline(
                user_id, 
                count = 1, 
                include_rts = False, 
                tweet_mode = "extended")[0]
        except ChunkedEncodingError:
            return {"valid": False, "output": f"User [{user_id}]: Could not read tweets. (ChunkEncodingError)", "sleep": True}
        except tw.TweepError as e:
            return {"valid": False, "output": f"User [{user_id}]: Could not read tweets. ({e})", "sleep": False}
        except:
            return {"valid": False, "output": f"User [{user_id}]: Could not read tweets.", "sleep": False}
        
        # Initialise pointers
        p1, p2 = (first_tweet.id, first_tweet.id)

        if first == p1: 
            # To resume where it was left off from last time...
            p2 = last

            # Ensure that what is stored is less than what to extract
            if tweets_to_extract <= stored_tweets:
                return {"valid": False, "output": f"User [{user_id}]: Skipping because attempting to extract less or the same amount of tweets than stored.", "sleep": False}
            else:
                tweets_to_extract -= stored_tweets
        else:
            # To restart process due to new tweets or never-seen-before user
            extracted_tweets.append(first_tweet)
            tweets_to_extract -= 1
            stored_tweets = 0

        while tweets_to_extract > 0:

            try:
                tweets = self.API.user_timeline(
                    user_id, 
                    count = REQUEST_LIMIT, 
                    include_rts = False, 
                    tweet_mode = "extended", 
                    max_id = p2 - 1)
            except:
                return {"valid": False, "output": f"User [{user_id}]: Something weird happened!", "sleep": True}

            # Break if there are no more tweets
            if len(tweets) == 0: 
                if len(extracted_tweets) == 0: 
                    return {"valid": False, "output": f"User [{user_id}]: No more tweets available than what's already stored.", "sleep": False}
                break

            p2 = tweets[-1].id
            extracted_tweets.extend(tweets)

            tweets_to_extract -= len(tweets)

        #* The reason why this is necessary is as follows:
        # Setting `include_rts` to False gives us less tweets than we actually specify. 
        # While we could send more API requests to make sure that we receive the exact amount we want, the increase in requests is not favourable.
        # Instead, we always request the REQUEST_LIMIT, and crop out the tweets that we don't need later (also fixing the last pointer).
        if tweets_to_extract < 0:
            extracted_tweets = extracted_tweets[:tweets_to_extract]
            p2 = extracted_tweets[-1].id

        document = self.textualise(extracted_tweets)

        return {"valid" : True, "output": {"text": document, "stored_tweets": len(extracted_tweets) + stored_tweets, "first": p1, "last": p2}, "sleep": False}