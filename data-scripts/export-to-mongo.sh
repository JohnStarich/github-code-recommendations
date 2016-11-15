#!/bin/bash

source utils.sh

cd "$(dirname $0)"

DATA_FILE=$1
if [ -z "$DATA_FILE" ]; then
    error 'Please provide a data file to export to MongoDB'
    exit 2
fi
if [ ! -f "$DATA_FILE" ]; then
    error "File $DATA_FILE does not exist"
    exit 2
fi

mongoimport -d github -c events <(gunzip -c "$DATA_FILE")

