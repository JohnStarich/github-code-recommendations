#!/bin/bash

cd "$(dirname $0)"
source utils.sh

while read line; do
    args=$(jq .id,.diff_url <<<$line | tr '"' ' ')
    id=$(awk '{ print $1 }' <<<$args)
    diff_url=$(awk '{ print $2 }' <<<$args)
    wget -O - "$diff_url" | node line-to-word-diff/index.js > "data/$id.diff"
done

