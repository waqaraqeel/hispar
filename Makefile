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

hispar-list-%: $(SRC)/get_list.sh $(ENGINE) $(TRANCO_DIR)/% 
	@rm -f $@ && touch $@
	$^ $(DOMAINS) $(URLS_PER_DOMAIN) $@

$(TRANCO_DIR)/%:
	@wget $(TRANCO_URL) -O $(TMP)/list.zip
	@unzip $(TMP)/list.zip -d $(TMP)/
	@tr -d '\r' < $(TMP)/top-1m.csv | tr ',' ' ' > $@
	@rm $(TMP)/list.zip $(TMP)/top-1m.csv

install:
	@apt-get install python3 python3-pip
	@pip3 install requests
	@sudo -u $$SUDO_USER mkdir -p $(TMP)
	@sudo -u $$SUDO_USER mkdir -p $(TRANCO_DIR)

clean:
	@rm -f hispar-list-$(TODAY) 