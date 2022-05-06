import pandas as panda
import requests
import math

bearer_token = 'AAAAAAAAAAAAAAAAAAAAADOHcAEAAAAAhGlt5ETi6uLI3oIFADPPWilii7c%3DakUXvErYQxMTHGUjdjxhhTKJhyFENNW4Z5ysKYjYFtdrdO18uT'  # os.environ.get("BEARER_TOKEN")

single_tweet_url = "https://api.twitter.com/2/tweets/"

# csv_path = 'G:\\test\\AllDetails.csv'
csv_path = 'G:\\test\\posts2copy.csv'
start_count = 1
end_count = 300


def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """
    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2RecentSearchPython"
    return r


def update_csv(min, max):
    df = panda.read_csv(csv_path, on_bad_lines='skip')
    kk = df.index.values[0]
    num_of_rows = len(df)

    print(df)
    if max > num_of_rows:
        max = num_of_rows

    for i in range(min, max):
        row = df.loc[[i]]
        formatted_id = '{0:18f}'.format(row['referenced_tweet_id'].values[0]).split(".")[0]
        vv1 = row['referenced_tweet_id'].values[0]
        print(formatted_id)
        if row['is_referenced_tweet'].values[0]:
            long_text = single_tweet(
                single_tweet_url + formatted_id + '?tweet.fields=created_at,text')
            if long_text != '':
                df.loc[i, 'text'] = long_text
                df.to_csv(csv_path, index=False)


def single_tweet(url):
    response = requests.get(url, auth=bearer_oauth)
    print(response.status_code)
    if response.json().get('data'):
        result = response.json()['data']
        if result.get('text'):
            return response.json()['data']['text']
        else:
            return ''
    else:
        return ''


def main():
    update_csv(start_count, end_count)


if __name__ == "__main__":
    main()
