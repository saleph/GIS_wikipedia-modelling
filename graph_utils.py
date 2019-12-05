# -*- coding: utf-8 -*-
import networkx as nx
import json
import os
import pathlib


def dump(G, filename):
    directory = pathlib.Path(filename).parent
    directory.mkdir(parents=True, exist_ok=True)
    nx.write_gpickle(G, filename)

def load(filename):
    G = None
    if os.path.isfile(filename):
        G = nx.read_gpickle(filename)
    return G
