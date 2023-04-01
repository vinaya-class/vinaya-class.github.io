LATEX=latexmk
LATEX_OPTS=-pdflua

all: vinaya-class-questions-A.pdf vinaya-class-questions-B.pdf vinaya-class-questions-A-answerkey.pdf vinaya-class-questions-B-answerkey.pdf

%.pdf: %.tex
	$(LATEX) $(LATEX_OPTS) $<

preview $(FILE):
	latexmk -pdflua -pvc -e '$$latex=q/latex %O -interaction=nonstopmode -halt-on-error %S/' $(FILE)

clean:
	rm -f *.aux *.log *.fdb_latexmk *.fls *.qsl *.cut *.sol *.pdf
