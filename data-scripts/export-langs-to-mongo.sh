#!/bin/bash

mongoimport -d github -c languages <(./mongo-lang-urls.sh | ./get-lang-stats.sh)
