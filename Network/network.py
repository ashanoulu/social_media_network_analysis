import csv
import networkx as nx
import matplotlib.pyplot as plt
# import scipy as sp
from networkx import *
from pandas import *

hashtags: list = []
G = nx.Graph()


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
    fig, ax = plt.subplots(figsize=(90, 60))
    # pos = nx.spring_layout(H, k=0.15, seed=4572321)
    pos = nx.kamada_kawai_layout(H)
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
    ax.set_title("Gene functional association network (C. elegans)", font)
    # Change font color for legend
    font["color"] = "r"
    ax.text(
        0.80,
        0.10,
        "node color = community structure",
        horizontalalignment="center",
        transform=ax.transAxes,
        fontdict=font,
    )
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
    return result/len(dc_dict)


def get_diameter():
    global G
    largest_connected_component = max(connected_components(G), key=len)
    largest_connected_graph = G.subgraph(largest_connected_component)
    return diameter(largest_connected_graph)


if __name__ == "__main__":
    add_nodes()
    add_edges()
    print(str("Number of Nodes =\t") + str(G.number_of_nodes()))
    print(str("Number of Edges =\t") + str(G.number_of_edges()))
    print(str("Average Degree Centrality =\t") + str(average_degree_centrality()))
    # print(str("Diameter =\t") + str(get_diameter()))

    plot_graph_2()


