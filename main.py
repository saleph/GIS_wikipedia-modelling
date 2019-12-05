import os
from adjacency_list_builder import generate_graph
import graph_utils


graph_cache_filename = "cache/graphmk.pickle"
dir_with_sql = "C:/Users/tomas/Downloads/data/"

pages = os.path.join(dir_with_sql, "mkwiki-latest-page.sql")
pagelinks = os.path.join(dir_with_sql, "mkwiki-latest-pagelinks.sql")

def printSomeThingsRegardingGraph(G):
    print("Nodes number:", len(G.nodes()))
    #graph_utils.plot_degrees_distribution(G)
    graph_utils.plot_clustering_coefficiences_distribution(G)

if __name__ == "__main__":
    G = graph_utils.load(graph_cache_filename)
    if G is None:
        G = generate_graph(pages, pagelinks)
        graph_utils.dump(G, graph_cache_filename)
    printSomeThingsRegardingGraph(G)
