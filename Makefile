SRC="README"
CSS_INCLUDE="css/bootstrap.min.css"
CSS_INCLUDE_PDF="bootstrap.min.css,pdf.css"
CSS_PATH='css'

all:
	@echo "targets: html"
html:
	rst2html.py --stylesheet=${CSS_INCLUDE} ${SRC}.rst > ${SRC}.html
pdf:
	rst2pdf --stylesheets=${CSS_INCLUDE_PDF} --stylesheet-path=${CSS_PATH} \
	-l ru_RU ${SRC}.rst > ${SRC}.pdf
clean:
	rm -f *.html
