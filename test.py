import tweepy

client = tweepy.Client(bearer_token = 'AAAAAAAAAAAAAAAAAAAAALDCcQEAAAAA0S%2BVPYHO9Asc1Hd5%2F3dVak0Nsew%3DmdbLOjr0JGcWjs0u93s4GUSOgH3WZxufFi0OsrdHpW04w7nd3W')

query = "#ukrainewar"
max_results = 10
tweet_fields = ['created_at', 'lang', 'public_metrics', 'referenced_tweets', 'text,entities', 'id', 'possibly_sensitive', 'source', 'withheld']

# Name and path of the file where you want the Tweets written to
file_name = 'tweets.txt'
index = 0

with open(file_name, 'a+', encoding='UTF8') as filehandle:
    for tweet in tweepy.Paginator(
            client.search_recent_tweets,
            query=query,
            tweet_fields=tweet_fields,
            max_results=max_results
    ).flatten(limit=1000):
        index += 1
        print(index)
        filehandle.write('%s\n' % tweet.text)
