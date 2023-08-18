all: chapters-to-tex vinaya-class-notes-pdf vinaya-class-questions-A-pdf vinaya-class-questions-B-pdf vinaya-class-questions-A-answerkey-pdf vinaya-class-questions-B-answerkey-pdf chanting-refcard-pdf schedule-pdf sign-up-sheet-pdf class-rules-pdf vinayakamma-chart-pdf sanghadisesa-procedure-pdf pali-lessons-pdf pali-cheatsheet-pdf pali-readings-pdf pali-lessons-anki-deck pali-readings-anki-deck vinaya-class-zip

dist:
	./scripts/dist.sh

chapters-to-tex:
	./scripts/chapters_to_tex.sh

chapters-to-docx:
	./scripts/chapters_to_docx.sh

vinaya-class-notes-pdf:
	./scripts/compile_tex.sh ./tex/vinaya-class-notes/vinaya-class-notes.tex

vinaya-class-questions-A-pdf:
	ANSWERKEY=FALSE ./scripts/compile_tex.sh ./tex/vinaya-class-questions/vinaya-class-questions-A.tex

vinaya-class-questions-B-pdf:
	ANSWERKEY=FALSE ./scripts/compile_tex.sh ./tex/vinaya-class-questions/vinaya-class-questions-B.tex

vinaya-class-questions-A-answerkey-pdf:
	ANSWERKEY=TRUE ./scripts/compile_tex.sh ./tex/vinaya-class-questions/vinaya-class-questions-A-answerkey.tex

vinaya-class-questions-B-answerkey-pdf:
	ANSWERKEY=TRUE ./scripts/compile_tex.sh ./tex/vinaya-class-questions/vinaya-class-questions-B-answerkey.tex

chanting-refcard-pdf:
	./scripts/compile_tex.sh ./tex/chanting-refcard/chanting-refcard.tex
	./scripts/compile_tex.sh ./tex/chanting-refcard/chanting-refcard-4on1.tex

schedule-pdf:
	./scripts/compile_tex.sh ./tex/schedule/schedule.tex

sign-up-sheet-pdf:
	./scripts/compile_tex.sh ./tex/schedule/sign-up-sheet.tex

class-rules-pdf:
	./scripts/compile_tex.sh ./tex/schedule/class-rules.tex

vinayakamma-chart-pdf:
	./scripts/compile_tex.sh ./tex/vinayakamma-chart/vinayakamma-chart.tex

sanghadisesa-procedure-pdf:
	./scripts/compile_tex.sh ./tex/sanghadisesa-procedure/sanghadisesa-procedure.tex

robe-keeping-pdf:
	./scripts/compile_tex.sh ./tex/robe-keeping/robe-keeping.tex

pali-vocabulary-words-pdf:
	cd tex/vinaya-class-questions && make pali-vocabulary-words

pali-vocabulary-sentences-pdf:
	cd tex/vinaya-class-questions && make pali-vocabulary-sentences

pali-lessons-pdf: pali-vocabulary-words-pdf pali-vocabulary-sentences-pdf
	cd tex/vinaya-class-questions && \
	make export-pali-lessons && \
	cd ../.. && \
	ANSWERKEY=FALSE ./scripts/compile_tex.sh ./tex/vinaya-class-questions/pali-lessons.tex && \
	ANSWERKEY=TRUE ./scripts/compile_tex.sh ./tex/vinaya-class-questions/pali-lessons-answerkey.tex

pali-cheatsheet-pdf:
	cd tex/vinaya-class-questions && \
	make export-pali-cheatsheet && \
	cd ../.. && \
	./scripts/compile_tex.sh ./tex/vinaya-class-questions/pali-cheatsheet.tex

pali-readings-pdf:
	cd tex/vinaya-class-questions && \
	make export-pali-readings && \
	cd ../.. && \
	./scripts/compile_tex.sh ./tex/vinaya-class-questions/pali-readings.tex

pali-lessons-anki-deck:
	cp tex/vinaya-class-questions/exported/pali-lessons.apkg src/includes/docs/pali-lessons.apkg

pali-readings-anki-deck:
	cp tex/vinaya-class-questions/exported/pali-readings.apkg src/includes/docs/pali-readings.apkg

vinaya-class-zip:
	cd src/includes/docs && zip vinaya-class.zip *.pdf *.apkg
