ALEXA_URL=http://s3.amazonaws.com/alexa-static/top-1m.csv.zip
ALEXA_DIR=alexa-lists
TMP=temp
SRC=src
DESTINATION=/home/waqar/hispar.cs.duke.edu/archive
GOOGLE=$(SRC)/google.py
BING=$(SRC)/bing.py

DOMAINS=1000
URLS_PER_DOMAIN=50
ENGINE=$(GOOGLE) # or $(BING)

TODAY=$(shell date +'%y-%m-%d')
YESTERDAY=$(shell date -d '-1 day' +'%y-%m-%d')

today: hispar-list-$(TODAY)
.SECONDARY:


hispar-list-%: $(SRC)/get_list.sh $(ENGINE) $(ALEXA_DIR)/% 
	$^ $(DOMAINS) $(URLS_PER_DOMAIN) $@ 1 50000

yesterday: $(SRC)/get_list.sh $(ENGINE) $(ALEXA_DIR)/$(YESTERDAY)
	OFFSET=$$((`tail -n 1 hispar-list-$(YESTERDAY) | cut -d" " -f1` + 1)) && \
	$^ $(DOMAINS) $(URLS_PER_DOMAIN) hispar-list-$(YESTERDAY) $$OFFSET 100000
	zip -9 hispar-list-$(YESTERDAY).zip hispar-list-$(YESTERDAY)
	mv hispar-list-$(YESTERDAY).zip $(DESTINATION)/

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
