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
    # data = read_csv(".\..\dataset.csv")
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
    # pos = nx.kamada_kawai_layout(G)
    # pos = nx.planar_layout(G)
    pos = nx.spring_layout(G, k=0.2)
    plt.figure(3, figsize=(50, 50))
    nx.draw(G, pos=pos)
    plt.show()
    plt.savefig('filename.png')


if __name__ == "__main__":
    add_nodes()
    add_edges()
    plot_graph()

