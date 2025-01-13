LATEX=latexmk
# LATEX_OPTS=-pdflua
LATEX_OPTS=-interaction=nonstopmode -halt-on-error -xelatex

all: vinaya-class-questions-A.pdf vinaya-class-questions-B.pdf vinaya-class-questions-A-answerkey.pdf vinaya-class-questions-B-answerkey.pdf pali-lessons.pdf

pali-vocabulary-chapters: export-vocabulary-lesson-1 vocabulary-lesson-1.pdf export-vocabulary-lesson-2 vocabulary-lesson-2.pdf

pali-vocabulary-words: export-vocabulary-words vocabulary-words.pdf

pali-vocabulary-sentences: export-vocabulary-sentences vocabulary-sentences.pdf

pali-lessons: export-pali-lessons pali-lessons.pdf

pali-cheatsheet: export-pali-cheatsheet pali-cheatsheet.pdf

pali-readings: export-pali-readings pali-readings.pdf

pali-readings-anki.zip:
	../../scripts/export-reading-vocab-to-anki.py ./pali-readings.org

pali-readings-upload: pali-readings pali-readings-anki.zip
	rclone copyto pali-readings.pdf "gambhiro.sumedharama:/Pāli Readings/pali-readings.pdf" && \
	rclone copyto pali-readings-anki.zip "gambhiro.sumedharama:/Pāli Readings/pali-readings-anki.zip"

pali-readings-with-sentence-analysis: export-pali-readings-with-sentence-analysis pali-readings-with-sentence-analysis.pdf

pali-readings-answerkey: export-pali-readings
	ANSWERKEY=TRUE make pali-readings-answerkey.pdf

pali-readings-with-sentence-analysis-answerkey: export-pali-readings-with-sentence-analysis
	ANSWERKEY=TRUE make pali-readings-with-sentence-analysis-answerkey.pdf

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

export-vocabulary-lesson-3:
	emacs --batch -L -l 'vocabulary-lesson-3.org' -l 'export-init.el' --eval '(progn (org-latex-export-to-latex))'

export-vocabulary-words:
	emacs --batch -L -l 'vocabulary-words.org' -l 'export-init.el' --eval '(progn (org-latex-export-to-latex))'

export-vocabulary-sentences:
	emacs --batch -L -l 'vocabulary-sentences.org' -l 'export-init.el' --eval '(progn (org-latex-export-to-latex))'

export-pali-cheatsheet:
	emacs --batch -L -l 'pali-cheatsheet.org' -l 'export-init.el' --eval '(progn (org-latex-export-to-latex))'

export-pali-readings:
	emacs --batch -L -l 'pali-readings.org' -l 'export-init.el' --eval '(progn (org-latex-export-to-latex))'

export-pali-readings-with-sentence-analysis:
	emacs --batch -L -l 'pali-readings-with-sentence-analysis.org' -l 'export-init.el' --eval '(progn (org-latex-export-to-latex))'

export-pali-readings-vocab-to-anki:
	../../scripts/export-vocab-org-to-anki.py ./pali-readings-with-sentence-analysis.org ./exported/pali-readings-with-sentence-analysis.apkg "Pāli Readings::7. The Weaver's Daughter (Dhp 174 and Commentary Story)::1. Vocabulary"

%.pdf: %.tex
	$(LATEX) $(LATEX_OPTS) $<

preview $(FILE):
	latexmk -pdflua -pvc -e '$$latex=q/latex %O -interaction=nonstopmode -halt-on-error %S/' $(FILE)

clean:
	rm -f *.aux *.log *.fdb_latexmk *.fls *.qsl *.cut *.sol *.pdf
