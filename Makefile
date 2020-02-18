ALEXA_URL=http://s3.amazonaws.com/alexa-static/top-1m.csv.zip
ALEXA_DIR=alexa-lists
TMP=temp
SRC=src
GOOGLE=$(SRC)/google.py
BING=$(SRC)/bing.py

DOMAINS=2000
URLS_PER_DOMAIN=50
ENGINE=$(GOOGLE) # or $(BING)

TODAY=$(shell date +'%y-%m-%d')
all: hispar-list-$(TODAY)
.SECONDARY:

hispar-list-%: $(SRC)/get_list.sh $(ENGINE) $(ALEXA_DIR)/% 
	@rm -f $@ && touch $@
	$^ $(DOMAINS) $(URLS_PER_DOMAIN) $@

$(ALEXA_DIR)/%:
	@wget $(ALEXA_URL) -O $(TMP)/list.zip
	@unzip $(TMP)/list.zip -d $(TMP)/
	@tr -d '\r' < $(TMP)/top-1m.csv | tr ',' ' ' > $@
	@rm $(TMP)/list.zip $(TMP)/top-1m.csv

install:
	@apt-get install python3 python3-pip
	@pip3 install requests
	@sudo -u $$SUDO_USER mkdir -p $(TMP)
	@sudo -u $$SUDO_USER mkdir -p $(ALEXA_DIR)

clean:
	@rm -f hispar-list-$(TODAY) 
