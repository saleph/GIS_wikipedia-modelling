import os
import sys
from adjacency_list_builder import generate_graph
import networkx as nx
import graph_utils
import json
import re

lang = "yi"
dir_with_sql = "C:/Users/tomas/Downloads/data/"


graph_cache_filename = "cache/graph{0}.pickle".format(lang)
graph_properties_filename = "cache/graph_properties{0}.pickle".format(lang)
BA_properties_filename = "cache/BA_properties_higher_order{0}.json".format(lang)
BA_properties_filename_10k = "cache/BA_properties_10k_nodes{0}.json".format(lang)
BA_properties_filename_37k = "cache/BA_properties_37k_nodes{0}.json".format(lang)
BA_modeling_yi_properties_filename = "cache/BA_modeling_yi_properties{0}.json".format(lang)
BA_modeling_yi_properties_filename_10k = "cache/BA_modeling_yi_10k_nodes_properties{0}.json".format(lang)
graph_geffi_filename = "cache/graph{0}.gexf".format(lang)
graph_BA_model_geffi_filename = "cache/graph_BA_model{0}.gexf".format(lang)
graph_BA_model_geffi_m100_filename = "cache/graph_BA_model_m100{0}.gexf".format(lang)
graph_BA_model_geffi_m50_filename = "cache/graph_BA_model_m50{0}.gexf".format(lang)
pages = os.path.join(dir_with_sql, "{0}wiki-latest-page.sql".format(lang))
pagelinks = os.path.join(dir_with_sql, "{0}wiki-latest-pagelinks.sql".format(lang))
seed = 1234

yi_nodes_no = 37712

def print_help():
    print('Usage: python3 main.py <path to -page.sql> <path to -pagelinks.sql> [check for avg shortest path]')
    print("Note: check for avg shortest path will take a lot of time! Consider using Gephi for that")
    print('Example: python3 main.py "packed_data/yiwiki-latest-page.sql" "packed_data/yiwiki-latest-pagelinks.sql" true')

def printSomeThingsRegardingGraph(G, check_shortest_path):
    if not check_shortest_path:
        print("Now some computation will be done. Will take approx. 2-3 minutes")
    else:
        print("Now some computation will be done. Will take approx. 40 minutes because of check_shortest_path method. Consider using generated geffi file in Gephi for shortest path checking")
    properties = graph_utils.get_properties(G, check_shortest_path)
    print("Graph properties")
    print('\n'.join([str(i) for i in properties.items()]))
    graph_utils.plot_degrees_distribution(G)
    #graph_utils.plot_clustering_coefficiences_distribution(G)

def analyze_ba_spectrum(nodes = 10000):
    ba_properties = dict()
    for m in range(10, 100, 10):
        ba_properties["m={}".format(m)] = analyze_ba(nodes, m)
    for m in range(100, 1000, 100):
        ba_properties["m={}".format(m)] = analyze_ba(nodes, m)
    for m in range(1000, 10000, 1000):
        ba_properties["m={}".format(m)] = analyze_ba(nodes, m)
    return ba_properties

def analyze_ba(nodes, m):
    print("Analysis of BA with m={}".format(m))
    props = graph_utils.get_properties(nx.barabasi_albert_graph(nodes, m, seed), check_shortest_path=False)
    print(json.dumps(props, indent=4))
    return props

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print_help()
        exit(1)
    pages = sys.argv[1]
    pagelinks = sys.argv[2]
    
    check_shortest_path = False
    if len(sys.argv) == 4:
        if re.match(r"true", sys.argv[3].strip(), re.IGNORECASE):
            check_shortest_path = True
    #graph_utils.dump_geffi(nx.barabasi_albert_graph(yi_nodes_no, 22), graph_BA_model_geffi_filename)
    #ba = analyze_ba(yi_nodes_no, 22)
    #graph_utils.dump_json(ba, BA_modeling_yi_properties_filename)
    #ba = analyze_ba_spectrum(yi_nodes_no)
    #graph_utils.dump_json(ba, BA_properties_filename_37k)
    #graph_utils.dump_geffi(nx.barabasi_albert_graph(yi_nodes_no, 50), graph_BA_model_geffi_m50_filename)

    G = graph_utils.load(graph_cache_filename)
    if G is None:
        G = generate_graph(pages, pagelinks, nx.Graph())
        graph_utils.dump(G, graph_cache_filename)
    graph_utils.dump_geffi(G, graph_geffi_filename)
    printSomeThingsRegardingGraph(G, check_shortest_path=check_shortest_path)
