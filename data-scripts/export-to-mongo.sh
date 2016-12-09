#!/bin/bash

cd "$(dirname $0)"

source utils.sh

DATA_FILES=$@
if [ -z "$DATA_FILES" ]; then
    error 'Please provide a data file to export to MongoDB'
    exit 2
fi

for data_file in $DATA_FILES; do
    if [ ! -f "$data_file" ]; then
        error "File $data_file does not exist"
        exit 2
    fi
    success "Importing $data_file"
    mongoimport -d github -c events <(gunzip -c "$data_file")
done
