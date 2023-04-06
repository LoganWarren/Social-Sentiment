import tweepy
import pandas as pd
import requests
from textblob import TextBlob
import os
from dotenv import load_dotenv

load_dotenv()

consumer_key = os.environ.get("CONSUMER_KEY")
consumer_secret = os.environ.get("CONSUMER_SECRET")
access_token = os.environ.get("ACCESS_TOKEN")
access_token_secret = os.environ.get("ACCESS_TOKEN_SECRET")

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

def fetch_tweets(query, count=100):
    tweets = []
    try:
        tweets = tweepy.Cursor(api.search_tweets, q=query, lang="en", tweet_mode="extended", count=count).items(count)
        return [tweet.full_text for tweet in tweets]
    except tweepy.TweepyException as e:
        print(f"Error: {e}")
        return tweets


def analyze_sentiment(tweets):
    sentiment_scores = []

    for tweet in tweets:
        analysis = TextBlob(tweet)
        sentiment_scores.append(analysis.sentiment.polarity)

    return sentiment_scores


def process_results(tweets, sentiment_scores):
    data = pd.DataFrame({'tweet': tweets, 'sentiment': sentiment_scores})
    data['sentiment_category'] = data['sentiment'].apply(lambda score: 'positive' if score > 0 else 'negative' if score < 0 else 'neutral')
    return data



def main():
    query = "example keyword"  # input desired query to search for
    tweet_count = 100

    tweets = fetch_tweets(query, tweet_count)
    sentiment_scores = analyze_sentiment(tweets)
    results = process_results(tweets, sentiment_scores)

    # Analyze and display the results
    print(results.head())
    print(results['sentiment_category'].value_counts())

if __name__ == "__main__":
    main()