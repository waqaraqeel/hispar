#!/usr/bin/env python3
import sys
import time
import requests
from config import bing_key, bing_url

import requests

headers = {"Ocp-Apim-Subscription-Key": bing_key, "BingAPIs-Market": "en-US"}

site_rank = int(sys.argv[1])
site = sys.argv[2]
file_ex = " ".join("-filetype:" + f for f in ("pdf", "doc", "txt"))
lang_loc = "language:en loc:us"
search_term = "site:" + " ".join((site, file_ex, lang_loc))
target = int(sys.argv[3])

PAGE_SIZE = min(50, target + 5)
offset = 0
uniques = set()

print(f"Getting landing page for {site}", file=sys.stderr)
landing = ""
try:
    resp = requests.get(f"http://{site}")
    landing = resp.url
except:
    pass

print(f"Searching {search_term}", file=sys.stderr)
printed = 0
landing_found = False

while printed < target:
    params = {
        "mkt": "en-US",
        "setLang": "en",
        "q": search_term,
        "count": PAGE_SIZE,
        "offset": offset,
        "responseFilter": ["Webpages"],
    }
    try:
        response = requests.get(bing_url, headers=headers, params=params, timeout=5)
        response.raise_for_status()
    except:
        break

    search_results = response.json()
    if "webPages" not in search_results:
        break

    for rank, ans in enumerate(search_results["webPages"]["value"]):
        url = ans["url"]
        if url not in uniques:
            uniques.add(ans["url"])
            if ans["url"] == landing:
                print(f"{site_rank} 0 {url}")
                landing_found = True
            elif printed == target - 1 and landing and not landing_found:
                break
            else:
                print(f"{site_rank} {offset + rank + 1} {url}")
            printed += 1
            if printed >= target:
                break

    print(f"Gathered {len(uniques)} results", file=sys.stderr)
    if len(search_results["webPages"]["value"]) < PAGE_SIZE - 5:
        break
    offset += len(search_results["webPages"]["value"])
    time.sleep(0.02)


if landing and not landing_found:
    print(f"{site_rank} 0 {landing}")