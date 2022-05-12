import csv
import networkx as nx
import matplotlib.pyplot as plt
# import scipy as sp
from pandas import *

hashtags: list = []
G = nx.Graph()


def add_nodes():
    global hashtags
    global G

    # data = read_csv("test.csv")
    data = read_csv("test2.csv")
    # data = read_csv(".\..\posts3.csv")
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
    print(hashtags)


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
        print(progress)


def plot_graph():
    global G
    # pos = nx.circular_layout(G)
    pos = nx.kamada_kawai_layout(G)
    plt.figure(3, figsize=(50, 50))
    # nx.draw(G)
    # nx.draw(G, with_labels=True, node_size=200, edgecolors='gray')
    nx.draw(G, pos=pos)
    plt.show()
    plt.savefig('filename.pdf')


if __name__ == "__main__":
    add_nodes()
    add_edges()
    plot_graph()

