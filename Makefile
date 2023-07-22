all: chapters-to-tex vinaya-class-notes-pdf vinaya-class-questions-A-pdf vinaya-class-questions-B-pdf vinaya-class-questions-A-answerkey-pdf vinaya-class-questions-B-answerkey-pdf chanting-refcard-pdf schedule-pdf sign-up-sheet-pdf class-rules-pdf vinayakamma-chart-pdf sanghadisesa-procedure-pdf pali-lessons-pdf pali-lessons-anki-deck vinaya-class-zip

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

pali-lessons-pdf:
	cd tex/vinaya-class-questions && \
	make export-pali-lessons && \
	cd ../.. && \
	ANSWERKEY=FALSE ./scripts/compile_tex.sh ./tex/vinaya-class-questions/pali-lessons.tex && \
	ANSWERKEY=TRUE ./scripts/compile_tex.sh ./tex/vinaya-class-questions/pali-lessons-answerkey.tex

pali-lessons-anki-deck:
	cp tex/vinaya-class-questions/vocabulary/exported/pali-lessons.apkg src/includes/docs/pali-lessons.apkg

vinaya-class-zip:
	cd src/includes/docs && zip vinaya-class.zip *.pdf *.apkg
