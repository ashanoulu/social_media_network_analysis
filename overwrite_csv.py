import pandas as panda
import requests
import math
import csv

bearer_token = 'AAAAAAAAAAAAAAAAAAAAALDCcQEAAAAA0S%2BVPYHO9Asc1Hd5%2F3dVak0Nsew%3DmdbLOjr0JGcWjs0u93s4GUSOgH3WZxufFi0OsrdHpW04w7nd3W'  # os.environ.get("BEARER_TOKEN")

multiple_tweet_url = "https://api.twitter.com/2/tweets?ids="
single_tweet_url = "https://api.twitter.com/2/tweets/"

# csv_path = 'G:\\test\\AllDetails.csv'
csv_path = 'dataset_small.csv'
file_header = ['hashtags']



def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """
    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2RecentSearchPython"
    return r


def update_csv(min, max, df):

    # df = panda.read_csv(csv_path, on_bad_lines='skip', dtype={'referenced_tweet_id': 'Int64'})
    kk = df.index.values[0]
    num_of_rows = len(df)

    print(df)
    if max > num_of_rows:
        max = num_of_rows

    id_list = ''
    for i in range(min, max):
        row = df.loc[[i]]
        if row['is_referenced_tweet'].values[0]:
            formatted_id = row['referenced_tweet_id'].values[0].split("TW")[1]
            if id_list == '':
                id_list = formatted_id
            id_list = id_list + ',' + formatted_id
            # print(formatted_id + " " + str(row['num'].values[0]))
            # long_text = single_tweet(
            #     single_tweet_url + formatted_id + '?tweet.fields=created_at,text')
            # if long_text != '':
            #     df.loc[i, 'text'] = long_text
            #     df.to_csv(csv_path, index=False)

    tweet_list = get_tweets(multiple_tweet_url + id_list + '&tweet.fields=created_at,text,entities,author_id')

    for i in range(min, max):
        row = df.loc[[i]]
        if row['is_referenced_tweet'].values[0]:
            formatted_id = row['referenced_tweet_id'].values[0].split("TW")[1]
            if tweet_list.get(formatted_id) is not None:
                df.loc[i, 'text'] = tweet_list.get(formatted_id).get('text')
                df.loc[i, 'hashtags'] = tweet_list.get(formatted_id).get('hashtags')
                df.loc[i, 'author_id'] = tweet_list.get(formatted_id).get('author_id')
                df.to_csv(csv_path, index=False)
    # with open('posts32.csv', 'w', encoding='UTF8', newline='') as f:
    #     writer = csv.writer(f)
    #     writer.writerows(df)


def get_tweets(url):
    request = requests.get(url, auth=bearer_oauth)
    response = request.json()
    print(response)
    tweets_dict = {}
    temp_response = request.status_code
    if request.status_code == 200:
        if response.get('data'):
            for tweet in response['data']:
                hashtags = ''
                if 'entities' in tweet.keys():
                    if tweet['entities'].get('hashtags'):
                        for hashtag in tweet['entities']['hashtags']:
                            hashtags = hashtags + ' ' + hashtag['tag']
                    tweets_dict[tweet['id']] = {'text': tweet['text'], 'hashtags': hashtags,
                                                'author_id': 'UID' + str(tweet['author_id'])}
    return tweets_dict
    #     if result.get('text'):
    #         return response.json()['data']['text']
    #     else:
    #         return ''
    # else:
    #     return ''


def extract_hashtags():
    data = panda.read_csv(csv_path, on_bad_lines='skip')
    hashtags = data['hashtags'].tolist()
    hashtag_list: list = []
    test_str = " test123 STRiNG"
    for row in hashtags:
        print(str(row))
        if str(row) != 'nan':
            hashtag_list.append(str(row).lower())
    with open('hashtags.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(file_header)
        for row in hashtag_list:
            writer.writerow([row])


def main():
    start_count = 0
    end_count = 100
    df = panda.read_csv(csv_path, on_bad_lines='skip')
    num_of_rows = len(df)
    while start_count < end_count:
        print(start_count, end_count)
        update_csv(start_count, end_count, df)
        start_count = start_count + 99
        end_count = end_count + 99
        if num_of_rows < end_count:
            end_count = num_of_rows
    # extract_hashtags()


if __name__ == "__main__":
    main()

# 11880 11980


