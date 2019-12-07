# -*- coding: utf-8 -*-
import networkx as nx
import json
import os
import pathlib
import matplotlib.pyplot as plt
import pylab

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
