## Hispar 100K
Hispar 100K is a research-oriented list of 100,000 web pages that can be used
for Internet measurements. It is the _first_ top list to provide URLs, and not
just domain names.

An example list, generated on January 27<sup>th</sup> 2020, has been included.
The first column is the [Alexa](https://www.alexa.com) rank of the domain, the
second column is the Google search result rank of the URL, and the third column
is the URL itself.

### Download
We prepare weekly lists of Top 100K URLs that can be downloaded
[here](http://hispar.cs.duke.edu).

### Methodology
We use the [Alexa list](https://www.alexa.com) to obtain the top one million
domains. Then, for each domain `d`, we query the Google Search API for the
search term `site:d`. Unique URLs from the search results are then added to the
list. We use top 2000 domains from the Tranco list, and at most 50 URLs for each
domain to prepare the Top 100K list. If there are fewer results for one or more
domains, and the final number of URLs does not add up to 100K, domains with rank
&gt; 2000 are processed in increasing rank order until we have 100K URLs.

### Build it yourself!
To generate Hispar using Google, you will need credentials for the [Google
Custom Search JSON
API](https://developers.google.com/custom-search/v1/overview). You will also
need to configure your endpoint to provide results for the entire web, and not
just a limited set of web sites. Please find instructions
[here](https://support.google.com/programmable-search/answer/4513886).

You can also use [Bing Web Search
API](https://azure.microsoft.com/en-us/services/cognitive-services/bing-web-search-api/).
Bing costs somewhat less than Google does.

Once you have the relevant credentials, please place them in
`src/config/__init__.py` as `google_key` and `google_cx`, or `bing_key` and
`bing_url`.

If you want to change the language or region settings for the search results,
please change the relevant query parameters in `google.py` or `bing.py`. The
number of domains to use, and the number of unique URLs to fetch for each domain
can be configured in the `Makefile`. 

To install the dependencies, simply run `sudo make install`. Otherwise, install
`requests` using `pip` (`python3` is required), and create the directories
`temp` and `alexa-lists` in the current directory.

To generate a list of URLs from today's Alexa list, run `make today`. The
generation is split into two parts because the Google API does not allow more
than 10,000 API requests per day. Once the request cap has been restored (day
changes in PST), run `make yesterday` to pick up from where it was paused
previously.
