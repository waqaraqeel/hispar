#!/bin/bash
ENGINE=$1
TRANCO_LIST=$2
DOMAINS=$3
URLS_PER_DOMAIN=$4
OUTPUT=$5
START=$6

TARGET=$(($DOMAINS * $URLS_PER_DOMAIN + $START * $URLS_PER_DOMAIN))
END=$(($START + $DOMAINS - 1))
sed -n "$START,$END p" $TRANCO_LIST | while read domain; do 
    $ENGINE $domain $URLS_PER_DOMAIN >> $OUTPUT
done

n=$(($END + 1))
while [[ `wc -l < $OUTPUT` -lt $TARGET ]]; do
    domain=`sed -n "${n}p" $TRANCO_LIST`
    $ENGINE $domain $URLS_PER_DOMAIN >> $OUTPUT
    n=$(($n + 1))
done
