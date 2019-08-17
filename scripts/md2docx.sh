#!/bin/bash

SRC="$1"
DEST="$2"

cat "$SRC" |\
# <!-- noexport_docx_begin --> ... <!-- noexport_docx_end -->
perl -0777 -pe "s/\n<!-- noexport_docx_begin -->\n(.*?)\n<!-- noexport_docx_end -->\n//gs" |\
pandoc -f markdown+raw_attribute-auto_identifiers -t docx --resource-path=./src --reference-doc=./scripts/reference.docx -o "$DEST"

