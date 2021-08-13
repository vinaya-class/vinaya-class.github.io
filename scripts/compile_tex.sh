#!/bin/bash

SRC_TEX="$1"
TARGET_PDF=$(echo -n "$SRC_TEX" | sed 's/\.tex$/.pdf/')
TARGET_PNG=$(echo -n "$SRC_TEX" | sed 's/\.tex$/-thumb.png/')

DOCS_DIR=./src/includes/docs

latexmk "$SRC_TEX" && cp "$TARGET_PDF" "$DOCS_DIR"
STATUS=$?

has_notify=0
if [ $(which notify-send) != "" ]; then
    has_notify=1
fi

if [ $has_notify -eq 1 ]; then
  convert -density 600 "$TARGET_PDF[0]" -flatten -resize 830x "$TARGET_PNG" && mv "$TARGET_PNG" "$DOCS_DIR"
fi

if [ $has_notify -eq 1 ]; then
    name=$(basename "$SRC_TEX")
    if [ $STATUS -eq 0 ]; then
        notify-send "OK: $name"
    else
        notify-send --urgency=critical "FAILURE: $name"
    fi
fi

