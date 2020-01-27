## Hispar 100K
Hispar 100K is a research-oriented list of web pages that can be used for
Internet measurements. It is the _first_ top list to provide URLs, and not just
domain names.

### Download
We prepare weekly lists of Top 100K URLs that can be downloaded
[here](http://hispar.cs.duke.edu).

### Methodology
We use the [Tranco list](https://tranco-list.eu) to obtain the top one million
domains. Then, for each domain &omega; we query the Bing Web Search API for the
search term `site:&omega;`. Unique URLs from the search results are then added
to the list. We use top 2000 domains from the Tranco list, and 50 URLs for each
domain to prepare the Top 100K list. If there are fewer results for one or more
domains, and the final number of URLs does not add up to 100K, domains with rank
&gt; 2000 are processed in increasing rank order until we have 100K URLs.

### Build it yourself!
To install the dependencies, simply run `sudo make install`. To generate a list
of URLs from today's Tranco list, run `make`.

The number of domains to use, and the number of unique URLs to fetch for each
domain can be configured in the `Makefile`. Google Custom Search API can also be
used, although it is more expensive. Bing Web Search credentials can be obtained
[here](https://azure.microsoft.com/en-us/services/cognitive-services/bing-web-search-api/).
Google Custom Search setup guide can be found
[here](https://developers.google.com/custom-search/docs/tutorial/introduction).
Google Custom Search will have to be configured to search the entire web, and
not just specific websites.