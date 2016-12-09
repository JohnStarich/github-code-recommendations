#!/bin/bash

source utils.sh

RATE_LIMIT=10

counter=1
while read line; do
    args=$(jq .id,.lastLanguage <<<$line | tr '"' ' ')
    language_url=$(awk '{ print $2 }' <<<$args)
    # echo $language_url
    # success "[$counter] Beginning processing on ID: $language_url"
    rate_limit "$RATE_LIMIT" \
        curl --user "wallyguzman:3d69d5b2f75668b826069b8c7a04068eb887c56e" \
            --silent "$language_url"
    counter=$(($counter + 1))
done
wait

