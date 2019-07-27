all: chapters-to-tex vinaya-class-notes-pdf chanting-refcard-pdf schedule-pdf vinayakamma-chart-pdf

dist:
	./helpers/dist.sh

chapters-to-tex:
	./helpers/chapters_to_tex.sh

vinaya-class-notes-pdf:
	./helpers/compile_tex.sh ./tex/vinaya-class-notes/vinaya-class-notes.tex

chanting-refcard-pdf:
	./helpers/compile_tex.sh ./tex/chanting-refcard/chanting-refcard.tex

schedule-pdf:
	./helpers/compile_tex.sh ./tex/schedule/schedule.tex

vinayakamma-chart-pdf:
	./helpers/compile_tex.sh ./tex/vinayakamma-chart/vinayakamma-chart.tex

