
input/HRC_Email_296.zip:
	mkdir -p input
	curl http://graphics.wsj.com/hillary-clinton-email-documents/zips/HRC_Email_296.zip -o input/HRC_Email_296.zip
input/HRCEmail_JuneWeb.zip:
	mkdir -p input
	curl http://graphics.wsj.com/hillary-clinton-email-documents/zips/HRCEmail_JuneWeb.zip -o input/HRCEmail_JuneWeb.zip
input/HRCEmail_JulyWeb.zip:
	mkdir -p input
	curl http://graphics.wsj.com/hillary-clinton-email-documents/zips/HRCEmail_JulyWeb.zip -o input/HRCEmail_JulyWeb.zip
input/Clinton_Email_August_Release.zip:
	mkdir -p input
	curl http://graphics.wsj.com/hillary-clinton-email-documents/zips/Clinton_Email_August_Release.zip -o input/Clinton_Email_August_Release.zip
INPUT_FILES=input/HRC_Email_296.zip input/HRCEmail_JuneWeb.zip input/HRCEmail_JulyWeb.zip input/Clinton_Email_August_Release.zip
input: $(INPUT_FILES)

working/pdfs/.sentinel: $(INPUT_FILES)
	mkdir -p working/pdfs
	unzip input/HRC_Email_296.zip -d working/pdfs/may
	unzip input/HRCEmail_JuneWeb.zip -d working/pdfs/june
	unzip input/HRCEmail_JulyWeb.zip -d working/pdfs/july
	unzip input/Clinton_Email_August_Release.zip -d working/pdfs/august
	touch working/pdfs/.sentinel
unzip: working/pdfs/.sentinel

working/text/.sentinel: working/pdfs/.sentinel
	mkdir -p working/text
	python scripts/pdftotext.py
	touch working/text/.sentinel
text: working/text/.sentinel

output/emails.csv: working/text/.sentinel
	mkdir -p output
	python scripts/extract_to_csv.py
csv: output/emails.csv

working/emailsNoHeader.csv: output/emails.csv
	tail +2 $^ > $@

output/database.sqlite: working/emailsNoHeader.csv
	sqlite3 -echo $@ < scripts/sqliteImport.sql

sqlite: output/database.sqlite

all: csv sqlite

clean:
	rm -rf working
	rm -rf output
