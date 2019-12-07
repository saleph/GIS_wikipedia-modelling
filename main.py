import os
from adjacency_list_builder import generate_graph
import graph_utils

lang = "yi"
dir_with_sql = "C:/Users/tomas/Downloads/data/"


graph_cache_filename = "cache/graph{0}.pickle".format(lang)
graph_geffi_filename = "cache/graph{0}.gexf".format(lang)
pages = os.path.join(dir_with_sql, "{0}wiki-latest-page.sql".format(lang))
pagelinks = os.path.join(dir_with_sql, "{0}wiki-latest-pagelinks.sql".format(lang))

def printSomeThingsRegardingGraph(G):
    print("Nodes number:", len(G.nodes()))
    graph_utils.plot_degrees_distribution(G)
    #graph_utils.plot_clustering_coefficiences_distribution(G)

if __name__ == "__main__":
    G = graph_utils.load(graph_cache_filename)
    if G is None:
        G = generate_graph(pages, pagelinks)
        graph_utils.dump(G, graph_cache_filename)
    #graph_utils.dump_geffi(G, graph_geffi_filename)
    printSomeThingsRegardingGraph(G)
