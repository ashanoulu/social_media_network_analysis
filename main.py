import requests
import os
import json
import csv
import time

file_header = ['num', 'hashtag', 'created_at', 'id', 'lang', 'source', 'like_count', 'quote_count', 'reply_count',
               'retweet_count', 'text', 'is_referenced_tweet', 'referenced_tweet_id', 'hashtags']
file_header_count = ['hashtag', 'count']

data_rows = []
data_rows_counter = []

# hash_tag_list = ['#ukraine', '#ukrainewar', '#war', '#army', '#military', '#kiev', '#ua', '#specialforces', '#donbass',
#                  '#donbasswar', '#airsoft', '#nomockal', '#warukraine', '#tactics', '#azovsea', '#militarystile',
#                  '#azov', '#russia', '#donetsk', '#soldiers', '#ukrainenews', '#odessa', '#ukrainianarmy', '#lviv',
#                  '#victory', '#nato', '#kyiv', '#militaryukraine', '#news', '#freesentso']

hash_tag_list = ['#ukraine', '#ukrainewar']

# To set your environment variables in your terminal run the following line:
# export 'BEARER_TOKEN'='<your_bearer_token>'
bearer_token = 'AAAAAAAAAAAAAAAAAAAAALDCcQEAAAAA0S%2BVPYHO9Asc1Hd5%2F3dVak0Nsew%3DmdbLOjr0JGcWjs0u93s4GUSOgH3WZxufFi0OsrdHpW04w7nd3W'  # os.environ.get("BEARER_TOKEN")

search_url = "https://api.twitter.com/2/tweets/search/all"
count_url = "https://api.twitter.com/2/tweets/counts/recent"
single_tweet_url = "https://api.twitter.com/2/tweets/"



def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """
    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2RecentSearchPython"
    return r


def connect_to_endpoint(url, params, hash_tag):
    retweet_count = 0
    response = requests.get(url, auth=bearer_oauth, params=params)
    print(response.status_code)

    i = 1
    if response.json().get('data'):
        for tweet in response.json()['data']:
            data_row: list = []

            data_row.append(i)
            data_row.append(hash_tag)
            data_row.append(tweet['created_at'])
            data_row.append('TW' + str(tweet['id']))
            data_row.append(tweet['lang'])
            data_row.append(tweet['source'])
            data_row.append(tweet['public_metrics']['like_count'])
            data_row.append(tweet['public_metrics']['quote_count'])
            data_row.append(tweet['public_metrics']['reply_count'])
            data_row.append(tweet['public_metrics']['retweet_count'])
            data_row.append(tweet['text'])

            if tweet.get('referenced_tweets'):
                retweet_count+=1
                data_row.append('true')
                data_row.append('TW' + str(tweet['referenced_tweets'][0]['id']))


                # data_row.append(single_tweet(single_tweet_url + tweet['referenced_tweets'][0]['id'] +'?tweet.fields=created_at,text'))
            else:
                data_row.append('false')
                data_row.append('')


            hashtags = ''
            if tweet['entities'].get('hashtags'):
                for hashtag in tweet['entities']['hashtags']:
                    hashtags = hashtags + ' ' + hashtag['tag']
                data_row.append(hashtags)
                print(hashtags)

            data_rows.append(data_row)
            data_row = []
            i = i + 1

    with open('posts3.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(file_header)
        writer.writerows(data_rows)

    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json(), retweet_count


def get_counts(url, params, hash_tag):
    response = requests.get(url, auth=bearer_oauth, params=params)
    print(response.status_code)

    if response.json().get('meta'):
        return [hash_tag, response.json()['meta']['total_tweet_count']]

    return response.json()


def single_tweet(url):
    response = requests.get(url, auth=bearer_oauth)
    print(response.status_code)
    result = response.json()['data']
    if result.get('text'):
        return response.json()['data']['text']
    else:
        return ''


def main():
    # with open('G:\\test\\posts.csv', 'w', encoding='UTF8', newline='') as f:
    #     writer = csv.writer(f)
    #     writer.writerow(file_header)
    #
    # with open('G:\\test\\count.csv', 'w', encoding='UTF8', newline='') as f:
    #     writer = csv.writer(f)
    #     writer.writerow(file_header_count)
    retweets = 0
    for hash_tag in hash_tag_list:
        query_params = {'query': hash_tag,
                        'tweet.fields': 'created_at,lang,public_metrics,referenced_tweets,text,entities,id,'
                                        'possibly_sensitive,source,withheld,attachments',
                        'max_results': 10
                        }

        counter_param = {'query': hash_tag}

        # count = get_counts(count_url, counter_param, hash_tag)
        # data_rows_counter.append(count)

        json_response, rt_count = connect_to_endpoint(search_url, query_params, hash_tag)
        retweets = retweets + rt_count
        print(json.dumps(json_response, indent=4, sort_keys=True))
        # print(json.dumps(json_response_counter, indent=4, sort_keys=True))
        time.sleep(1)

    with open('count.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(file_header_count)
        writer.writerows(data_rows_counter)

    print(retweets)

if __name__ == "__main__":
    main()

