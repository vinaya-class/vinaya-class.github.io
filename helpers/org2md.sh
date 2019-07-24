#!/bin/bash

SRC="$1"
DEST="$2"

cat "$SRC" |\
# quote marks
sed -e 's/``/"/g; s/'"''"'/"/g; s/`/'"'"'/g;' |\
# convert definition list to plain list
sed -e 's/^- \([^:]\+\) *:: *\(.*\)/- *\1,* \2/; s/ \+\(,\*\)/\1/;' |\
# clean spaces and remove repeated blanks
sed 's/^ *$//' |\
cat -s |\
pandoc -f org+smart -t markdown+smart-fenced_divs --atx-headers -o "$DEST"

