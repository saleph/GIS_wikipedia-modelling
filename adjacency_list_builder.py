# -*- coding: utf-8 -*-
import re
import json
import os.path
import pathlib
from collections import defaultdict

def generate_pages_links():
    first_phase_json_cache_links = 'cache1/1st_phase_links.json'
    first_phase_json_cache_title_cache = 'cache1/1st_phase_title_cache.json'
    second_phase_json_cache_links = 'cache1/2nd_phase_links_FULL_SOLUTION.json'
    dir_with_sql = "C:/Users/tomas/Downloads/data/"

    links = defaultdict(dict) # links[namespace_id][page_id] = {namespace_id:[1,4,5]}
    title_cache = defaultdict(dict)

    pathlib.Path('cache1').mkdir(exist_ok=True)

    if os.path.isfile(second_phase_json_cache_links):
        print("Full solution cache available. Reading the pages with links, will take a long time...")
        with open(second_phase_json_cache_links, 'r') as f:
            links = json.load(f)
    else:
        if os.path.isfile(first_phase_json_cache_links) and os.path.isfile(first_phase_json_cache_title_cache):
            print("Cache available. Reading the pages without links...")
            with open(first_phase_json_cache_links, 'r') as f:
                links = json.load(f)
            print("Reading title to id lookup table...")
            with open(first_phase_json_cache_title_cache, 'r') as f:
                title_cache = json.load(f)
            print("Cache successfully restored")
        else:
            print("No cache available")
            pages_pattern = re.compile("\\((\d+),(.+?),'(.*?)',.*?,NULL\\)")
            with open(dir_with_sql + "plwiki-latest-page.sql", "r", encoding="utf8") as file:
                print("Start of the pages processing (around 3100k)")
                counter = 0
                for line in file:
                    for match in re.finditer(pages_pattern, line):
                        page_id = int(match.group(1))
                        namespace_id = int(match.group(2))
                        title = match.group(3)
                        links[namespace_id][page_id] = defaultdict(list)
                        title_cache[namespace_id][title] = page_id

                        counter += 1
                        if counter % 100000 == 0:
                            print("Pages processed: " + str(counter//1000) + "k")

            print("Pages processed. Caching pages...")
            with open(first_phase_json_cache_links, 'w') as fp:
                json.dump(links, fp)
            print("Pages cached. Caching title to id lookup table...")
            with open(first_phase_json_cache_title_cache, 'w') as fp:
                json.dump(title_cache, fp)
            print("All the caching done")

        pattern_links = re.compile("\\((\d+),(\d+),'(.*?)',(\d+)\\)[,;]")
        with open(dir_with_sql + "plwiki-latest-pagelinks.sql", "r", encoding="utf8") as file:
            print("Start of the links processing (around 158kk)")
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
                        links[from_namespace][from_id][to_namespace].append(to_id)
                    except:
                        # links may be invalid, as stated: https://www.mediawiki.org/wiki/Manual:Pagelinks_table
                        continue

                    counter += 1
                    if counter % 1000000 == 0:
                        print("Links processed: " + str(counter//1000000) + "kk")

        print("Links processed. Caching pages with links...")
        with open(second_phase_json_cache_links, 'w') as fp:
            json.dump(links, fp)
        print("Caching done")
    return links
