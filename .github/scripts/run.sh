#!/bin/bash

set -euo pipefail

if [ -z "${OUTPUT_FILE:-}" ]; then
    echo "ERROR: OUTPUT_FILE environment variable is not set" >&2
    exit 1
fi


poetry run scrapy crawl centris-plex -O "${OUTPUT_FILE}"
