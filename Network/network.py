import csv
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
# import scipy as sp
import pandas as panda
from networkx import *
from networkx.algorithms.community.label_propagation import label_propagation_communities
from pandas import *
import botometer

hashtags: list = []
G = nx.Graph()
csv_path = '.\..\hashtags.csv'


def add_nodes():
    global hashtags
    global G

    # data = read_csv("test.csv")
    # data = read_csv("test2.csv")
    data = read_csv(".\..\hashtags.csv")
    hashtag_column = data['hashtags'].tolist()
    split_row: list = []

    for row in hashtag_column:
        if str(row) != 'nan':
            split_row = row.split(" ")
            split_row.pop(0)
            hashtags.append(split_row)
            # print(split_row)
        for tag in split_row:
            G.add_node(tag)
    # print(hashtags)


def add_edges():
    global hashtags
    global G
    progress = 0
    for row in hashtags:
        for tag in row:
            for i in range(0, len(row)):
                if tag != row[i]:
                    G.add_edge(tag, row[i])
        progress += 1
        # print(progress)


def plot_graph():
    global G
    # pos = nx.circular_layout(G)
    # pos = nx.kamada_kawai_layout(G)
    # pos = nx.planar_layout(G)
    pos = nx.spring_layout(G, k=0.1)
    plt.figure(3, figsize=(50, 50))
    nx.draw(G, pos=pos)
    plt.show()
    plt.savefig('filename.png')


def plot_graph_2():
    global G
    largest_connected_component = max(connected_components(G), key=len)
    H = G.subgraph(largest_connected_component)
    b_centrality = nx.betweenness_centrality(H, k=10, endpoints=True)

    #### draw graph ####
    fig, ax = plt.subplots(figsize=(40, 30))
    pos = nx.spring_layout(H, k=0.15, seed=4572321)
    node_size = [v * 20000 for v in b_centrality.values()]
    nx.draw_networkx(
        H,
        pos=pos,
        with_labels=False,
        node_size=node_size,
        edge_color="gainsboro",
        alpha=0.7,
    )
    # Title/legend
    font = {"color": "k", "fontweight": "bold", "fontsize": 20}
    ax.set_title("Social Network Graph", font)
    # Change font color for legend
    font["color"] = "r"
    ax.text(
        0.80,
        0.06,
        "node size = betweeness centrality",
        horizontalalignment="center",
        transform=ax.transAxes,
        fontdict=font,
    )
    # Resize figure for label readibility
    ax.margins(0.1, 0.05)
    fig.tight_layout()
    plt.axis("off")
    plt.show()


def average_degree_centrality():
    global G
    result = 0.00
    dc_dict = degree_centrality(G)
    for val in dc_dict.values():
        result += val
    return result / len(dc_dict)


def get_diameter():
    global G
    largest_connected_component = max(connected_components(G), key=len)
    largest_connected_graph = G.subgraph(largest_connected_component)
    return diameter(largest_connected_graph)


def plot_degree_distribution():
    global G
    plt.figure(figsize=(12, 8))

    degree_freq = nx.degree_histogram(G)
    degrees = range(len(degree_freq))
    plt.loglog(degrees[0:], degree_freq[0:], 'go-')
    plt.xlabel('Degree')
    plt.ylabel('Frequency')
    plt.show()


def plot_clustering():
    global G
    plt.figure(figsize=(12, 8))

    clustering_coeff = clustering(G)
    coeff_list = clustering_coeff.values()
    print(coeff_list)
    plt.hist(coeff_list)
    plt.xlabel('Clustering Coefficient')
    plt.ylabel('Frequency')
    plt.show()


def apply_botometer():
    global G
    dc_dict = degree_centrality(G)
    top_nodes = list(sorted(dc_dict.items(), key=lambda item: item[1], reverse=True))[:10]
    # print(top_nodes)
    df = panda.read_csv(csv_path, on_bad_lines='skip')
    num_of_rows = len(df)
    top_node_data_dict = {}
    for i in range(0, num_of_rows):
        row = df.loc[[i]]
        hashtag_list = str(row['hashtags'].values[0]).upper().split(' ')
        for top_node in top_nodes:
            node_name = top_node[0].upper()
            if node_name in hashtag_list:
                if top_node_data_dict.get(node_name) is not None:
                    ee = top_node_data_dict.get(node_name)
                    top_node_data_dict.get(node_name).append(str(row['user_id'].values[0].split('UID')[1]))
                else:
                    id_list = []
                    id_list.append(str(row['user_id'].values[0].split('UID')[1]))
                    top_node_data_dict[node_name] = id_list

    for tag in top_node_data_dict:
        print(str(tag) + str(len(top_node_data_dict[tag])) + str(top_node_data_dict[tag]))

    rapidapi_key = "d9b7a4190cmsh38c6c796119704dp1dc402jsn906b12a1df42"
    twitter_app_auth = {
        'consumer_key': 'WyFMw1QulAnTP5ZaN9R2GJW2O',
        'consumer_secret': 'wYBqkFEkFMmV1G308VmUdJtN1rKFq30Ejet3fm029fIxbI2JTA',
        'access_token': '1522681302008442880-LWEon8S6BEMpI0JDSrSZysDa8ut5iT',
        'access_token_secret': 'mNzHQX88vazrCI8naMgl5hkTcQ06EEU5ajnuToRikEuzu',
    }
    bom = botometer.Botometer(wait_on_ratelimit=True, rapidapi_key=rapidapi_key, **twitter_app_auth)

    bot_count = 0
    normal_users = 0
    tags = []
    normal_user_count_list = []
    bot_count_list = []
    csv_rows = []
    for tag_node in top_node_data_dict:
        try:
            bot_measurements = bom.check_accounts_in(top_node_data_dict[tag_node])
            # bot_measurements = bom.check_accounts_in([1378016874424905735, 795402912151244800])
            for result in bot_measurements:
                if result[1]['cap']['universal'] > 0.81:
                    bot_count = bot_count + 1
                else:
                    normal_users = normal_users + 1

                print(result[1]['cap']['universal'])
        except Exception as e:
            print(str(e))
        finally:
            tags.append(tag_node)
            normal_user_count_list.append(normal_users)
            bot_count_list.append(bot_count)
            data_row = []
            data_row.append(tag_node)
            data_row.append(normal_users)
            data_row.append(bot_count)
            csv_rows.append(data_row)
            bot_count = 0
            normal_users = 0
            break

        tags.append(tag_node)
        normal_user_count_list.append(normal_users)
        bot_count_list.append(bot_count)
        data_row = []
        data_row.append(tag_node)
        data_row.append(normal_users)
        data_row.append(bot_count)
        csv_rows.append(data_row)
        bot_count = 0
        normal_users = 0

    file_header = ['tag', 'normal_users', 'bot_users']

    with open('bot.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(file_header)
        writer.writerows(csv_rows)
    width = 0.35  # the width of the bars: can also be len(x) sequence

    fig, ax = plt.subplots()

    ax.bar(tags, normal_user_count_list, width, label='Normal Users')
    ax.bar(tags, bot_count_list, width, bottom=normal_user_count_list, label='Bot Users')

    ax.set_ylabel('Count')
    ax.set_title('Count by bot/normal users')
    ax.legend()

    plt.show()

    # data_row: list = []
    #
    # data_row.append(i)
    # data_row.append(row['hashtag'].values[0])
    # data_row.append(row['created_at'].values[0])
    # data_row.append(row['id'].values[0])
    # data_row.append(row['lang'].values[0])
    # data_row.append(row['source'].values[0])
    # data_row.append(row['like_count'].values[0])
    # data_row.append(row['quote_count'].values[0])
    # data_row.append(row['reply_count'].values[0])
    # data_row.append(row['retweet_count'].values[0])
    # data_row.append(row['text'].values[0])
    # data_row.append(row['author_id'].values[0])
    # data_row.append(row['is_referenced_tweet'].values[0])
    # data_row.append(row['referenced_tweet_id'].values[0])
    # data_row.append(row['hashtags'].values[0])
    # csv_data.append(data_row)
    # break

    # file_header = ['num', 'hashtag', 'created_at', 'id', 'lang', 'source', 'like_count', 'quote_count', 'reply_count',
    #                'retweet_count', 'text', 'author_id', 'is_referenced_tweet', 'referenced_tweet_id', 'hashtags']
    #
    # with open('top_node_data.csv', 'w', encoding='UTF8', newline='') as f:
    #     writer = csv.writer(f)
    #     writer.writerow(file_header)
    #     writer.writerows(csv_data)


def label_propagation():
    global G

    communities = label_propagation_communities(G)
    print(len(communities))
    csv_data = []
    for vals in communities:
        print(vals)
        H = G.subgraph(vals)
        graph_edges = H.number_of_edges()
        graph_nodes = H.number_of_nodes()
        graph_diameter = diameter(H.subgraph(max(connected_components(H), key=len)))
        clust_coeff = average_clustering(H, count_zeros=True)
        data_row = []
        hash_tags = ''
        for val in vals:
            hash_tags = hash_tags + str(val) + ' '

        data_row.append(graph_edges)
        data_row.append(graph_nodes)
        data_row.append(graph_diameter)
        data_row.append(clust_coeff)
        data_row.append(hash_tags)
        csv_data.append(data_row)

        print(
            str('Number of Edges = ') + str(graph_edges) +
            str(', Number of Nodes = ') + str(graph_nodes) +
            str(', Graph Diameter = ') + str(graph_diameter) +
            str(', Clustering Coefficient = ') + str(clust_coeff)
        )

    file_header = ['edges', 'nodes', 'diameter', 'coefficient', 'hashtags']
    with open('communities.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(file_header)
        writer.writerows(csv_data)


if __name__ == "__main__":
    add_nodes()
    add_edges()
    print(str("Number of Nodes =\t") + str(G.number_of_nodes()))
    print(str("Number of Edges =\t") + str(G.number_of_edges()))
    print(str("Average Degree Centrality =\t") + str(average_degree_centrality()))
    print(str("Average Clustering Coefficient =\t") + str(average_clustering(G, count_zeros=True)))
    # print(str("Diameter =\t") + str(get_diameter()))
    # plot_degree_distribution()
    # plot_clustering()
    # label_propagation()
    apply_botometer()
    # plot_graph_2()
