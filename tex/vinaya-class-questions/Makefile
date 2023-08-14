LATEX=latexmk
# LATEX_OPTS=-pdflua
LATEX_OPTS=-interaction=nonstopmode -halt-on-error -xelatex

all: vinaya-class-questions-A.pdf vinaya-class-questions-B.pdf vinaya-class-questions-A-answerkey.pdf vinaya-class-questions-B-answerkey.pdf pali-lessons.pdf

pali-vocabulary-chapters: export-vocabulary-lesson-1 vocabulary-lesson-1.pdf export-vocabulary-lesson-2 vocabulary-lesson-2.pdf

pali-vocabulary-words: export-vocabulary-words vocabulary-words.pdf

pali-vocabulary-sentences: export-vocabulary-sentences vocabulary-sentences.pdf

pali-lessons: export-pali-lessons pali-lessons.pdf

pali-cheatsheet: export-pali-cheatsheet pali-cheatsheet.pdf

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

export-vocabulary-lesson-2:
	emacs --batch -L -l 'vocabulary-lesson-2.org' -l 'export-init.el' --eval '(progn (org-latex-export-to-latex))'

export-vocabulary-words:
	emacs --batch -L -l 'vocabulary-words.org' -l 'export-init.el' --eval '(progn (org-latex-export-to-latex))'

export-vocabulary-sentences:
	emacs --batch -L -l 'vocabulary-sentences.org' -l 'export-init.el' --eval '(progn (org-latex-export-to-latex))'

export-pali-cheatsheet:
	emacs --batch -L -l 'pali-cheatsheet.org' -l 'export-init.el' --eval '(progn (org-latex-export-to-latex))'

%.pdf: %.tex
	$(LATEX) $(LATEX_OPTS) $<

preview $(FILE):
	latexmk -pdflua -pvc -e '$$latex=q/latex %O -interaction=nonstopmode -halt-on-error %S/' $(FILE)

clean:
	rm -f *.aux *.log *.fdb_latexmk *.fls *.qsl *.cut *.sol *.pdf
