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
    nx.write_gpickle(G, filename)

def load(filename):
    G = None
    if os.path.isfile(filename):
        G = nx.read_gpickle(filename)
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
