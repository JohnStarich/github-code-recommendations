#!/bin/bash

cd "$(dirname $0)"
source utils.sh

mongo --quiet github lang-urls.js 
