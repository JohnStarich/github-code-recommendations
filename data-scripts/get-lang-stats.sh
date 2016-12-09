#!/bin/bash

source utils.sh

RATE_LIMIT=10

counter=1
while read language_url; do
    success "[$counter] Beginning processing on URL: $language_url"
    rate_limit "$RATE_LIMIT" \
        curl --user 'JohnStarich:6aa4d28b107fb57bd879c2f6e62a31f5c7680937' \
            --silent \
            "$language_url" \| \
        mongoimport -d github -c languages
    counter=$(($counter + 1))
done
wait

