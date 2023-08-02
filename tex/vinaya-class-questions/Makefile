LATEX=latexmk
# LATEX_OPTS=-pdflua
LATEX_OPTS=-interaction=nonstopmode -halt-on-error -xelatex

all: vinaya-class-questions-A.pdf vinaya-class-questions-B.pdf vinaya-class-questions-A-answerkey.pdf vinaya-class-questions-B-answerkey.pdf pali-lessons.pdf

pali-vocabulary: export-vocabulary-lesson-1 vocabulary-lesson-1.pdf

pali-lessons: export-pali-lessons pali-lessons.pdf

pali-lessons-answerkey: export-pali-lessons
	ANSWERKEY=TRUE make pali-lessons-answerkey.pdf

pali-lessons-preview:
	ANSWERKEY=FALSE ./pali-lessons-preview.sh

pali-lessons-answerkey-preview:
	ANSWERKEY=TRUE ./pali-lessons-preview.sh

export-pali-lessons:
	emacs --batch -L -l 'pali-lessons.org' -l 'export-init.el' --eval '(progn (org-latex-export-to-latex))'

export-vocabulary-lesson-1:
	emacs --batch -L -l 'vocabulary-lesson-1.org' -l 'export-init.el' --eval '(progn (org-latex-export-to-latex))'

%.pdf: %.tex
	$(LATEX) $(LATEX_OPTS) $<

preview $(FILE):
	latexmk -pdflua -pvc -e '$$latex=q/latex %O -interaction=nonstopmode -halt-on-error %S/' $(FILE)

clean:
	rm -f *.aux *.log *.fdb_latexmk *.fls *.qsl *.cut *.sol *.pdf
