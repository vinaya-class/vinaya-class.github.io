# change to local dir
$do_cd = 1;

# always compile, ignore timestamps
$go_mode = 1;

# 4 means compile to pdf with lualatex
$pdf_mode = 4;
$lualatex = 'lualatex -interaction=nonstopmode -halt-on-error %O %S';
$postscript_mode = $dvi_mode = 0;

$pdf_previewer = 'evince %O %S';

