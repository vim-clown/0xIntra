import time

import Intra

while Intra.active:

    def search_tweets(q, count=1):
        return Intra.intra_api.search_tweets(
            q=q
            + " -giveaway -LIKEFOLLOWANDRETWEET! -#NFTGiveaway -towin -away -retweet -airdrop -drop -RT", # tags to be avoided
            result_type="recent",
            count=count,
            tweet_mode="extended",
        )

    def retweet_tweet(tweet):
        try:
            tag_list = []
            for tag in tweet.entities["hashtags"]:
               tag_list.append(tag) 
            if [
                medium["type"] == "photo" or "video"
                for medium in tweet.entities["media"]
            ] and [
                medium["text"] != "giveaway" for medium
                in tweet.entities["hashtags"]
            ] and hasattr(tweet, "user_mentions") == False and len(tag_list) <= 3: # to avoid tweets with spammy tags
                result = Intra.intra_api.retweet(tweet.id)
                tweet_text = result.text
                print(f"Retweeted: {tweet_text}")
                return result
            else:
                print("not accepted")
                return None
        except Intra.TwitterHTTPError as e:
            print("Error: ", e)
            return None
        except KeyError as keyerror:
            print("Error:", keyerror)
            return None

    def auto_retweet(q, count):
        result = search_tweets(q, count)
        success = 0
        print("looping through statuses")
        for tweet in result:
            if retweet_tweet(tweet) is not None:
                success += 1
        print(f"retweeted {success} tweet(s)")
        if success == 0:
            time.sleep(10)
        else:
            time.sleep(600)

    read_file = Intra.codecs.open("Intra/list.txt", "r+", "utf-8")
    content = read_file.readlines()
    wordlist = [i for i in content]
    read_file.close()
    
    for word in range(len(wordlist)):
        auto_retweet(wordlist[word], 1)
 
