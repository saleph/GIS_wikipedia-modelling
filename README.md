# GIS_wikipedia-modelling
Study project. We'll analyze wikipedia pagelinks graph and find most similar graph model, which will model this graph as close as possible.

## Preparation
1.
```bash
python3 -m pip install requirements.txt
```

2.
Unzip the data from directory packed_data (using 7zip).

## Run
```bash
python3 main.py <path to -page.sql> <path to -pagelinks.sql> [check for avg shortest path]
python3 main.py "packed_data/yiwiki-latest-page.sql" "packed_data/yiwiki-latest-pagelinks.sql"
```
