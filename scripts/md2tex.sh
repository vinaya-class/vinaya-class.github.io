#!/bin/bash

SRC="$1"
DEST="$2"

cat "$SRC" |\
# recognize mindmaps by path
# ![Pr-2](./includes/mindmaps/pr-2.png)
# \includemap{../src/includes/mindmaps/pr-2.png}
sed 's/^![[][^]]*[]](\.\/\(includes\/mindmaps\/[^)]\+\))/\`\`\`{=latex}\n\\includemap{..\/..\/src\/\1}\n\`\`\`/' |\
# direct includegraphics for figures
sed 's/^![[][^]]*[]](\.\/\(includes\/figures\/[^)]\+\))/\`\`\`{=latex}\n\\includegraphics{..\/..\/src\/\1}\n\`\`\`/' |\
# <!-- noexport_latex_begin --> ... <!-- noexport_latex_end -->
perl -0777 -pe "s/\n<!-- noexport_latex_begin -->\n(.*?)\n<!-- noexport_latex_end -->\n//gs" |\
# <!-- latex ... -->
perl -0777 -pe "s/\n<!-- latex\n(.*?)\n-->\n/\n\`\`\`{=latex}\n\1\n\`\`\`\n/gs" |\
pandoc -f markdown+raw_attribute-auto_identifiers -t latex --top-level-division=chapter -o "$DEST"
# add a trailing blank
echo >> "$DEST"

