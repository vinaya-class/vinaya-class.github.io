all: chapters-to-tex vinaya-class-notes-pdf chanting-refcard-pdf schedule-pdf vinayakamma-chart-pdf sanghadisesa-procedure-pdf

dist:
	./scripts/dist.sh

chapters-to-tex:
	./scripts/chapters_to_tex.sh

chapters-to-docx:
	./scripts/chapters_to_docx.sh

vinaya-class-notes-pdf:
	./scripts/compile_tex.sh ./tex/vinaya-class-notes/vinaya-class-notes.tex

vinaya-class-questions-pdf:
	./scripts/compile_tex.sh ./tex/vinaya-class-questions/vinaya-class-questions.tex

vinaya-class-questions-answerkey-pdf:
	./scripts/compile_tex.sh ./tex/vinaya-class-questions/vinaya-class-questions-answerkey.tex

chanting-refcard-pdf:
	./scripts/compile_tex.sh ./tex/chanting-refcard/chanting-refcard.tex
	./scripts/compile_tex.sh ./tex/chanting-refcard/chanting-refcard-4on1.tex

schedule-pdf:
	./scripts/compile_tex.sh ./tex/schedule/schedule.tex

sign-up-sheet-pdf:
	./scripts/compile_tex.sh ./tex/schedule/sign-up-sheet.tex

vinayakamma-chart-pdf:
	./scripts/compile_tex.sh ./tex/vinayakamma-chart/vinayakamma-chart.tex

sanghadisesa-procedure-pdf:
	./scripts/compile_tex.sh ./tex/sanghadisesa-procedure/sanghadisesa-procedure.tex

robe-keeping-pdf:
	./scripts/compile_tex.sh ./tex/robe-keeping/robe-keeping.tex