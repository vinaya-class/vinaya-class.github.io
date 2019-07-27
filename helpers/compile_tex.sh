#!/bin/bash

SRC_TEX="$1"
TARGET_PDF=$(echo -n "$SRC_TEX" | sed 's/\.tex$/.pdf/')

DOCS_DIR=./src/includes/docs

latexmk "$SRC_TEX" && cp "$TARGET_PDF" "$DOCS_DIR"
STATUS=$?

has_notify=0
if [ $(which notify-send) != "" ]; then
    has_notify=1
fi

if [ $has_notify -eq 1 ]; then
    name=$(basename "$SRC_TEX")
    if [ $STATUS -eq 0 ]; then
        notify-send "OK: $name"
    else
        notify-send --urgency=critical "FAILURE: $name"
    fi
fi

