#!/bin/bash

set -euo pipefail

# check if we have one argument
if [ $# -ne 1 ]
  then
    echo "Provide one arguments. Usage ./run.sh path-to-file.json" >&2
    exit 1
fi

ARG_OUTPUT_FILE="$1"

poetry run scrapy crawl centris-plex -O "${ARG_OUTPUT_FILE}"
