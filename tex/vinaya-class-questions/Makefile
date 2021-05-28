LATEX=latexmk
LATEX_OPTS=-pdflua

all: 00-introduction-questions.pdf 01-killing-and-harming-questions.pdf 02-stealing-questions.pdf 03-sexual-conduct-questions.pdf 04-lustful-conduct-questions.pdf 05-women-1-questions.pdf 06-attainments-questions.pdf 07-false-speech-questions.pdf 11-food-1-questions.pdf

%.pdf: %.tex
	$(LATEX) $(LATEX_OPTS) $<

preview $(FILE):
	latexmk -pdflua -pvc -e '$$latex=q/latex %O -interaction=nonstopmode -halt-on-error %S/' $(FILE)

clean:
	rm -f *.aux *.log *.fdb_latexmk *.fls *.qsl *.cut *.sol *.pdf
