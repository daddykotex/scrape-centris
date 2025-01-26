#!/bin/bash

set -euo pipefail

CURRENT_DATETIME=$(date +"%Y%m%d_%H%M%S")
OUTPUT_FILE="listings_${CURRENT_DATETIME}.json"


if [ -n "${CI:-}" ]; then
    echo "Setting OUTPUT_FILE environment variable" >&2
    echo "OUTPUT_FILE=${OUTPUT_FILE}" >> "$GITHUB_ENV"
fi

poetry run scrapy crawl centris-plex -O "${OUTPUT_FILE}"
