TRANCO_URL=https://tranco-list.eu/download_daily/5JYN
TRANCO_DIR=tranco-lists
TMP=temp
SRC=src
GOOGLE=$(SRC)/google.py
BING=$(SRC)/bing.py

DOMAINS=2000
URLS_PER_DOMAIN=50
ENGINE=$(BING) # or $(BING)

TODAY=$(shell date +'%y-%m-%d')
all: hispar-list-$(TODAY)
.SECONDARY:

hispar-list-%: $(ENGINE) $(TRANCO_DIR)/% 
	@rm -f $@
	@head -n $(DOMAINS) $(TRANCO_DIR)/$* | tr -d '\r' | tr ',' ' ' | \
		while read domain; do \
			$< $$domain $(URLS_PER_DOMAIN) >> $@; \
		done

$(TRANCO_DIR)/%:
	@wget $(TRANCO_URL) -O $(TMP)/list.zip
	@unzip $(TMP)/list.zip -d $(TMP)/ && mv $(TMP)/top-1m.csv $@
	@rm $(TMP)/list.zip

install:
	@apt-get install python3 python3-pip
	@pip3 install requests

clean:
	@rm -f hispar-list-$(TODAY) 