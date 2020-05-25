#!/usr/bin/env python3
import sys
import time
from config import google_key, google_cx

import requests

search_url = "https://www.googleapis.com/customsearch/v1"
MAX_RESULTS = 100

site_rank = int(sys.argv[1])
KEY, CX = google_key, google_cx

site = sys.argv[2]
file_ex = " ".join("-filetype:" + f for f in ("pdf", "doc", "txt"))
search_term = "site:" + " ".join((site, file_ex))
target = int(sys.argv[3])
if target > MAX_RESULTS:
    sys.exit(f"More than {MAX_RESULTS} results for one query not supported")

PAGE_SIZE = min(10, target + 5)
offset = 1
uniques = set()

print(f"Getting landing page for {site}", file=sys.stderr)
landing = ""
try:
    resp = requests.get(f"http://{site}", timeout=5)
    landing = resp.url
except:
    pass
if not landing:
    print("Could not get landing page", file=sys.stderr)
    exit(0)
    
results = []
print(f"Searching {search_term}", file=sys.stderr)
landing_found = False
last_len = 0

while len(uniques) < target:
    params = {
        "key": KEY,
        "cx": CX,
        "q": search_term,
        "gl": "us",
        "cr": "countryUS",
        "lr": "lang_en",
        "num": PAGE_SIZE,
        "start": offset
    }
    try:
        response = requests.get(search_url, params=params, timeout=5)
        response.raise_for_status()
    except:
        break

    search_results = response.json()
    if "items" not in search_results:
        break

    for rank, ans in enumerate(search_results["items"]):
        url = ans["link"]
        if url not in uniques:
            uniques.add(url)
            if url == landing:
                results.append(f"{site_rank} 0 {url}")
                # print(f"{site_rank} 0 {url}")
                landing_found = True
            elif len(uniques) == target - 1 and landing and not landing_found:
                break
            else:
                results.append(f"{site_rank} {offset + rank} {url}")
                # print(f"{site_rank} {offset + rank} {url}")
            if len(uniques) >= target:
                break

    print(f"Gathered {len(uniques)} results", file=sys.stderr)
    if len(uniques) - last_len  < PAGE_SIZE / 3:
        break
    last_len = len(uniques)
    offset += len(search_results["items"])
    time.sleep(1)


if landing and not landing_found:
    results.append(f"{site_rank} 0 {landing}")
    # print(f"{site_rank} 0 {landing}")

if len(results) > 10:
    for r in results:
        print(r)
