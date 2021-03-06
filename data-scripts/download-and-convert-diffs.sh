#!/bin/bash

cd "$(dirname $0)"
source utils.sh

# The maximum number of concurrent tasks to run at a time.
RATE_LIMIT=10

counter=1
while read line; do
    args=$(jq .id,.diff_url <<<$line | tr '"' ' ')
    id=$(awk '{ print $1 }' <<<$args)
    success "[$counter] Beginning processing on ID: $id"
    diff_url=$(awk '{ print $2 }' <<<$args)
    rate_limit "$RATE_LIMIT" \
        curl --user 'JohnStarich:6aa4d28b107fb57bd879c2f6e62a31f5c7680937' \
            --silent --output - --location \
            "$diff_url" \| \
        awk '"length($0) < 1000"' \| \
        node line-to-word-diff/index.js "$id"
    counter=$(($counter + 1))
done
wait
