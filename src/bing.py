#!/usr/bin/env python3
import sys
import time
from config import bing_key, bing_url

import requests

headers = {"Ocp-Apim-Subscription-Key": bing_key}

site_rank = int(sys.argv[1])
search_term = "site:" + sys.argv[2]
target = int(sys.argv[3])

# site_rank = 2
# search_term = "site:twitter.com"
# target = 1000

PAGE_SIZE = min(target, 50)
offset = 0
tries = 0
uniques = set()
results = []

print(f"Searching {search_term}", file=sys.stderr)
while len(uniques) < target and tries < target/PAGE_SIZE * 5:
    params = {
        "q": search_term,
        "textDecorations": True,
        "textFormat": "HTML",
        "count": PAGE_SIZE,
        "offset": offset,
        "responseFilter": ["Webpages"],
    }
    response = requests.get(bing_url, headers=headers, params=params)
    response.raise_for_status()
    search_results = response.json()
    if "webPages" not in search_results:
        break
    for rank, ans in enumerate(search_results["webPages"]["value"]):
        url = ans["url"]
        if url not in uniques:
            uniques.add(ans["url"])
            results.append((offset + rank + 1, url))
    print(f"Gathered {len(uniques)} results", file=sys.stderr)
    offset += len(search_results["webPages"]["value"])
    tries += 1
    time.sleep(0.05)

for r in results[:target]:
    print(f"{site_rank} {r[0]} {r[1]}")
