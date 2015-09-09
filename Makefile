
working/pdfs/.sentinel:
	mkdir working/pdfs
	unzip input/Clinton_Email_August_Release.zip -d working/pdfs/august
	unzip input/HRCEmail_JulyWeb.zip -d working/pdfs/july
	unzip input/HRCEmail_JuneWeb.zip -d working/pdfs/june
	unzip input/HRC_Email_296.zip -d working/pdfs/may
	touch working/pdfs/.sentinel
unzip: working/pdfs/.sentinel

working/text/.sentinel: working/pdfs/.sentinel
	mkdir working/text
	python scripts/pdftotext.py
	touch working/text/.sentinel
text: working/text/.sentinel

working/emails.csv:
	python scripts/extract_to_csv.py
csv: working/emails.csv

clean:
	rm -rf working
	mkdir working
