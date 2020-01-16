# -*- coding: utf-8 -*-
import networkx as nx
import json
import os
import pathlib
import matplotlib.pyplot as plt
import pylab
from operator import itemgetter
from statistics import mean 

def load_json(filename):
    if not os.path.isfile(filename):
        print("There is no cached {0}".format(filename))
        return None

    with open(filename, 'r') as f:
        return json.load(f)

def dump_json(dictionary, filename):
    with open(filename, 'w') as f:
        f.write(json.dumps(dictionary, indent=4))

def get_properties(G, check_shortest_path=False):
    print("Getting properties")

    avg_path_len=None
    if check_shortest_path:
        print("Get avg shortest path")
        if nx.is_connected(G):
            avg_path_len = nx.average_shortest_path_length(G)
        else:
            avg_path_len = mean([nx.average_shortest_path_length(G.subgraph(nodes)) for nodes in nx.connected_components(G)])

    print("Get nodes number")
    nodes_number = len(G.nodes())
    print(nodes_number)

    print("Get avg degree")
    avg_deg = mean([d for n, d in G.degree])
    print(avg_deg)

    print("Get avg clustering coeff")
    avg_clustering = nx.average_clustering(G)
    print(avg_clustering)

    return dict(
        nodes_number=nodes_number,
        avg_deg=avg_deg,
        avg_clustering=avg_clustering,
        avg_path_len=avg_path_len
    )

def dump(G, filename):
    directory = pathlib.Path(filename).parent
    directory.mkdir(parents=True, exist_ok=True)
    print("Dumping the graph into pickle in", filename)
    nx.write_gpickle(G, filename)
    print("Dumping sucessful")

def dump_geffi(G, filename):
    directory = pathlib.Path(filename).parent
    directory.mkdir(parents=True, exist_ok=True)
    print("Dumping the graph into gexf format in", filename)
    nx.write_gexf(G, filename)
    print("Dumping sucessful")

def load(filename):
    print("Loading pickled graph from", filename)
    if not os.path.isfile(filename):
        print("There is no cached graph")
        return None
    G = nx.read_gpickle(filename)
    print("Graph loaded from pickle")
    return G

def plot_degrees_distribution(G):
    degs = [deg for (node, deg) in G.degree()]
    degs.sort(reverse=True)
    plt.plot(degs)
    plt.ylabel('degree')
    plt.yscale('log')
    plt.xscale('log')
    plt.show()

def plot_clustering_coefficiences_distribution(G):
    coef = [deg for (node, deg) in nx.algorithms.cluster.clustering(G)]
    coef.sort(reverse=True)
    plt.plot(coef)
    plt.ylabel('clustering_coefficiences')
    plt.yscale('log')
    plt.xscale('log')
    plt.show()

def draw(G):
    # nx.draw_shell(G, with_labels=True, font_weight='bold')
    # plt.show()
    print("Start drawing the graph...")
    node_and_degree = G.degree()
    (largest_hub, degree) = sorted(node_and_degree, key=itemgetter(1))[-1]
    # Create ego graph of main hub
    hub_ego = nx.ego_graph(G, largest_hub)
    # Draw graph
    pos = nx.spring_layout(hub_ego)
    nx.draw(hub_ego, pos, node_color='b', node_size=10, with_labels=False)
    # Draw ego as large and red
    nx.draw_networkx_nodes(hub_ego, pos, nodelist=[largest_hub], node_size=50, node_color='r')
    plt.show()