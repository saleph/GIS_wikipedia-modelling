# -*- coding: utf-8 -*-
import networkx as nx
import json


def generate_graph_from_links(links):
    G = nx.Graph()    
    for namespace_id, pages_in_namespace in links.items():
        for page_id, page_links in pages_in_namespace.items():
            from_node = (namespace_id, page_id)
            for to_namespace_id, to_page_ids in page_links.items():
                for to_page_id in to_page_ids:
                    to_node = (to_namespace_id, to_page_id)
                    G.add_edge(from_node, to_node)
    return G

def cache_graph(G, filename):
    with open(filename, 'w') as fp:
        json.dump(G, fp)

def read_from_cache(filename):
    G = None
    if os.path.isfile(filename):
        with open(filename, 'r') as f:
            G = json.load(f)
    return G