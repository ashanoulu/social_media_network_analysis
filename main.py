import requests
import os
import json
import csv

file_header = ['hashtag', 'created_at', 'id', 'lang', 'source', 'like_count', 'quote_count', 'reply_count',
               'retweet_count', 'text', 'hashtags']
file_header_count = ['hashtag', 'count']

data_rows = []
data_rows_counter = []

hash_tag_list = ['#ukrainewar', '#war', '#army', '#military', '#kiev', '#ua', '#specialforces', '#donbass',
                 '#donbasswar', '#airsoft', '#nomockal', '#warukraine', '#tactics', '#azovsea', '#militarystile',
                 '#azov', '#russia', '#donetsk', '#soldiers', '#ukrainenews', '#odessa', '#ukrainianarmy', '#lviv',
                 '#victory', '#nato', '#kyiv', '#militaryukraine', '#news', '#freesentso']
# To set your environment variables in your terminal run the following line:
# export 'BEARER_TOKEN'='<your_bearer_token>'
bearer_token = 'AAAAAAAAAAAAAAAAAAAAADOHcAEAAAAAhGlt5ETi6uLI3oIFADPPWilii7c%3DakUXvErYQxMTHGUjdjxhhTKJhyFENNW4Z5ysKYjYFtdrdO18uT'  # os.environ.get("BEARER_TOKEN")

search_url = "https://api.twitter.com/2/tweets/search/recent"
count_url = "https://api.twitter.com/2/tweets/counts/recent"


def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """
    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2RecentSearchPython"
    return r


def connect_to_endpoint(url, params, hash_tag):
    response = requests.get(url, auth=bearer_oauth, params=params)
    print(response.status_code)

    if response.json().get('data'):
        for tweet in response.json()['data']:
            data_row: list = []

            data_row.append(hash_tag)
            data_row.append(tweet['created_at'])
            data_row.append(tweet['id'])
            data_row.append(tweet['lang'])
            data_row.append(tweet['source'])
            data_row.append(tweet['public_metrics']['like_count'])
            data_row.append(tweet['public_metrics']['quote_count'])
            data_row.append(tweet['public_metrics']['reply_count'])
            data_row.append(tweet['public_metrics']['retweet_count'])
            data_row.append(tweet['text'])

            if tweet['entities'].get('hashtags'):
                for hashtag in tweet['entities']['hashtags']:
                    data_row.append(hashtag['tag'])
                print(tweet['lang'])

            data_rows.append(data_row)
            data_row = []

    with open('G:\\test\\posts.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(file_header)
        writer.writerows(data_rows)

    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()


def get_counts(url, params, hash_tag):

    response = requests.get(url, auth=bearer_oauth, params=params)
    print(response.status_code)

    if response.json().get('meta'):
        return [hash_tag, response.json()['meta']['total_tweet_count']]

    return response.json()


def main():
    # with open('G:\\test\\posts.csv', 'w', encoding='UTF8', newline='') as f:
    #     writer = csv.writer(f)
    #     writer.writerow(file_header)
    #
    # with open('G:\\test\\count.csv', 'w', encoding='UTF8', newline='') as f:
    #     writer = csv.writer(f)
    #     writer.writerow(file_header_count)

    for hash_tag in hash_tag_list:
        query_params = {'query': hash_tag,
                        'tweet.fields': 'created_at,lang,public_metrics,referenced_tweets,text,entities,id,'
                                        'possibly_sensitive,source,withheld,attachments',
                        'max_results': 100
                        }

        counter_param = {'query': hash_tag}

        count = get_counts(count_url, counter_param, hash_tag)
        data_rows_counter.append(count)

        # json_response = connect_to_endpoint(search_url, query_params, hash_tag)
        # print(json.dumps(json_response, indent=4, sort_keys=True))
        # print(json.dumps(json_response_counter, indent=4, sort_keys=True))

    with open('G:\\test\\count.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(file_header_count)
        writer.writerows(data_rows_counter)

if __name__ == "__main__":
    main()
