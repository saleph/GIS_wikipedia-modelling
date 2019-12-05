from adjacency_list_builder import generate_pages_links
import graph_utils

graph_cache_filename = "cache1/graph.json"

def printSomeThingsRegardingLinks(links):
    namespaces_sizes = [len(pages_in_namespace) for pages_in_namespace in links.values()]
    print("Number of pages with links stored: " + str(sum(namespaces_sizes)))

    first_namespace_dict = list(links.values())[0]
    first_page_links_per_namespace = list(first_namespace_dict.values())[0]
    print("first_page_links_per_namespace:")
    for namespace_id, page_links in first_page_links_per_namespace.items():
        print("namespace:", namespace_id, page_links)

def printSomeThingsRegardingGraph(G):
    print("Nodes number:", len(G.nodes()))

if __name__ == "__main__":
    G = graph_utils.read_from_cache(graph_cache_filename)
    if G is None:
        links = generate_pages_links()
        #printSomeThingsRegardingLinks(links)
        G = graph_utils.generate_graph_from_links(links)
        graph_utils.cache_graph(G, graph_cache_filename)
    printSomeThingsRegardingGraph(G)
