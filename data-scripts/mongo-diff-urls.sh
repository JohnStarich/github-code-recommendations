#!/bin/bash

cd "$(dirname $0)"
source utils.sh

mongo --quiet github diff-urls.js 
