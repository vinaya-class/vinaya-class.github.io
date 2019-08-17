#!/bin/bash

DEST_DIR="./docx"

for i in ./src/[0-9][0-9]-*.md; do
    name=$(basename "$i" .md)

    if [ "$name" == "00-vinaya-class" ]
    then
        continue
    fi

    ./scripts/md2docx.sh "$i" "$DEST_DIR/$name.docx"
done
