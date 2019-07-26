#!/bin/bash

DEST_DIR="./tex/vinaya-class-notes/chapters"

for i in ./src/[0-9][0-9]-*.md; do
    name=$(basename "$i" .md)
    ./helpers/md2tex.sh "$i" "$DEST_DIR/$name.tex"
done
