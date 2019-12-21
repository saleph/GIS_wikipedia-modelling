# -*- coding: utf-8 -*-
import re
import json
import os.path
import pathlib
from collections import defaultdict
import networkx as nx

def generate_graph(pages, pagelinks, G=nx.Graph()):
    title_cache = _prepare_title_cache(pages)
    G = _prepare_graph(pagelinks, title_cache, G)   
    return G

def _prepare_title_cache(pages):
    title_cache = defaultdict(dict)
    pages_pattern = re.compile("\\((\\d+),(.+?),'(.*?)',.*?,NULL\\)")
    with open(pages, "r", encoding="utf8") as file:
        print("Start of the pages processing")
        counter = 0
        for line in file:
            for match in re.finditer(pages_pattern, line):
                page_id = int(match.group(1))
                namespace_id = int(match.group(2))
                title = match.group(3)
                title_cache[namespace_id][title] = page_id

                counter += 1
                if counter % 10000 == 0:
                    print("Pages processed: " + str(counter//1000) + "k")
    print("Pages processed")
    return title_cache

def _prepare_graph(pagelinks, title_cache, G):
    pattern_links = re.compile("\\((\\d+),(\\d+),'(.*?)',(\\d+)\\)[,;]")
    print("Start of the links processing and graph generation")
    with open(pagelinks, "r", encoding="utf8") as file:
        counter = 0
        for line in file:
            for match in re.finditer(pattern_links, line):
                from_id = int(match.group(1))
                from_namespace = int(match.group(4))
                to_namespace = int(match.group(2))
                to_title = match.group(3)
                to_id = None
                try:
                    to_id = title_cache[to_namespace][to_title]
                except:
                    # links may be invalid, as stated: https://www.mediawiki.org/wiki/Manual:Pagelinks_table
                    continue
                from_node = (from_namespace, from_id)
                to_node = (to_namespace, to_id)
                G.add_edge(from_node, to_node)

                counter += 1
                if counter % 100000 == 0:
                    print("Links processed: " + str(counter//1000) + "k")
    print("Links processed, graph generated")
    return G