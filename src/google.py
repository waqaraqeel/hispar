#!/usr/bin/env python3
import sys
import time
from config import google_key, google_cx

import requests

search_url = "https://www.googleapis.com/customsearch/v1"
MAX_RESULTS = 100

site_rank = int(sys.argv[1])
search_term = "site:" + sys.argv[2]
target = int(sys.argv[3])
if target > MAX_RESULTS:
    sys.exit(f"More than {MAX_RESULTS} results for one query not supported")

PAGE_SIZE = min(target, 10)
offset = 0
tries = 0
uniques = set()
results = []

print(f"Searching {search_term}", file=sys.stderr)
while len(uniques) < target and tries < target/PAGE_SIZE * 5 and offset + PAGE_SIZE < MAX_RESULTS:
    params = {
        "key": google_key,
        "cx": google_cx,
        "q": search_term,
        "gl": "us",
        "num": PAGE_SIZE,
        "start": offset
    }
    response = requests.get(search_url, params=params)
    response.raise_for_status()
    search_results = response.json()
    for rank, ans in enumerate(search_results["items"]):
        url = ans["link"]
        if url not in uniques:
            uniques.add(url)
            results.append((offset + rank + 1, url))
    print(f"Gathered {len(uniques)} results", file=sys.stderr)
    offset += len(search_results["items"])
    tries += 1
    time.sleep(1)

for r in results[:target]:
    print(f"{site_rank} {r[0]} {r[1]}")
