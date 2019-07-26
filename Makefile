LATEX_CMD=lualatex -interaction=nonstopmode -halt-on-error

TEX_DOCS_DIR=../../src/includes/docs

all: vinaya-class-notes-pdf chanting-refcard-pdf schedule-pdf vinayakamma-chart-pdf

build-html:
	mdbook build

chapters-to-tex:
	./helpers/chapters_to_tex.sh

vinaya-class-notes-pdf:
	cd tex/vinaya-class-notes && \
	$(LATEX_CMD) vinaya-class-notes.tex && \
	$(LATEX_CMD) vinaya-class-notes.tex && \
	cp vinaya-class-notes.pdf $(TEX_DOCS_DIR)

chanting-refcard-pdf:
	cd tex/chanting-refcard && \
	$(LATEX_CMD) chanting-refcard.tex && \
	$(LATEX_CMD) chanting-refcard.tex && \
	cp chanting-refcard.pdf $(TEX_DOCS_DIR)

schedule-pdf:
	cd tex/schedule && \
	$(LATEX_CMD) schedule.tex && \
	$(LATEX_CMD) schedule.tex && \
	cp schedule.pdf $(TEX_DOCS_DIR)

vinayakamma-chart-pdf:
	cd tex/vinayakamma-chart && \
	$(LATEX_CMD) vinayakamma-chart.tex && \
	$(LATEX_CMD) vinayakamma-chart.tex && \
	cp vinayakamma-chart.pdf $(TEX_DOCS_DIR)
