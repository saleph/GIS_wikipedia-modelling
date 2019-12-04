# -*- coding: utf-8 -*-
import re
import json
import os.path
from collections import defaultdict

first_phase_json_cache_pages = 'pages_after_first_step.json'
first_phase_json_cache_title_cache = 'title_cache_after_first_step.json'
second_phase_json_cache_pages = 'pages_after_second_step.json'

pages = defaultdict(dict) # pages[namespace_id][page_id] = {'page_title':"someTitle", adj_list=[(namespace_id, page_id), (namespace_id, page_id)]}
title_cache = defaultdict(dict) # pages[namespace_id][page_id] = {'page_title':"someTitle", adj_list=[(namespace_id, page_id), (namespace_id, page_id)]}

#tworzenie listy węzłów w postaci słownika
pages_pattern = re.compile("\\((\d+),(.+?),'(.*?)',.*?,NULL\\)")

if os.path.isfile(second_phase_json_cache_pages):
    print("Full solution cache available. Reading the pages...")
    with open(first_phase_json_cache_pages, 'r') as f:
        pages = json.load(f)
else
    if os.path.isfile(first_phase_json_cache_pages) and os.path.isfile(first_phase_json_cache_title_cache):
        print("Cache available. Reading the pages...")
        with open(first_phase_json_cache_pages, 'r') as f:
            pages = json.load(f)
        print("Reading title to id lookup table...")
        with open(first_phase_json_cache_title_cache, 'r') as f:
            title_cache = json.load(f)
        print("Cache successfully restored")
    else:
        print("No cache available")
        with open("data/plwiki-latest-page.sql", "r", encoding="utf8") as file:
            counter = 0
            for line in file:
                for match in re.finditer(pages_pattern, line):
                    page_id = int(match.group(1))
                    namespace_id = int(match.group(2))
                    title = match.group(3)
                    pages[namespace_id][page_id] = dict(page_title=title, adj_list=list())
                    title_cache[namespace_id][title] = page_id

                    counter += 1
                    if counter % 10000 == 0:
                        print("Pages processed: " + str(counter//1000) + "k")

        print("Pages processed. Caching pages...")
        with open(first_phase_json_cache_pages, 'w') as fp:
            json.dump(pages, fp)
        print("Pages cached. Caching title to id lookup table...")
        with open(first_phase_json_cache_title_cache, 'w') as fp:
            json.dump(title_cache, fp)
        print("All the caching done")

        pattern_links = re.compile("\\((\d+),(\d+),'(.*?)',(\d+)\\)[,;]")

        with open("data/plwiki-latest-pagelinks.sql", "r", encoding="utf8") as file:
            counter = 0
            for line in file:
                for match in re.finditer(pattern_links, line):
                    from_id = int(match.group(1))
                    from_namespace = int(match.group(4))
                    to_namespace = int(match.group(2))
                    to_title = match.group(3)

                    to_id = 0
                    try:
                        to_id = title_cache[to_namespace][to_title]
                    except:
                        # links may be invalid, as stated: https://www.mediawiki.org/wiki/Manual:Pagelinks_table
                        continue
                    try:
                        pages[from_namespace][from_id]['adj_list'].append((to_namespace, to_id))
                    except:
                        continue

                    counter += 1
                    if counter % 10000 == 0:
                        print("Links processed: " + str(counter//1000) + "k")

        with open(second_phase_json_cache_pages, 'w') as fp:
            json.dump(pages, fp)



print("Number of pages stored: " + str(len(pages)))