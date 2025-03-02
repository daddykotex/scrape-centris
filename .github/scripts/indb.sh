#!/bin/bash

set -euo pipefail


# check if we have at least two arguments
if [ $# -ne 2 ]
  then
    echo "Provide two arguments. Usage ./indb.sh path-to-db.db path-to-file.json" >&2
    exit 1
fi

ARG_DB="$1"
ARG_JSON="$2"

ARG_JSON_NAME=$(basename "$ARG_JSON")
ARG_TABLE_NAME="${ARG_JSON_NAME%.*}"

echo "$ARG_DB and $ARG_JSON"

# shellcheck disable=SC2016
FLATTEN_JQ='[.[] | [paths(scalars) as $path | {"key": $path | join("_"), "value": getpath($path)}] | from_entries]'

jq "$FLATTEN_JQ" "$ARG_JSON" | poetry run sqlite-utils insert "$ARG_DB" "$ARG_TABLE_NAME" --pk=property_id -
