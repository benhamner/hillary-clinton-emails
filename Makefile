
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
input/metadata.csv:
	mkdir -p input
	python scripts/metadata.py
input: $(INPUT_FILES) input/metadata.csv

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

input/emailsNoId.csv: working/text/.sentinel input/metadata.csv
	python scripts/emailsNoId.py

output/emails.csv: input/emailsNoId.csv
	mkdir -p output
	python scripts/persons.py
output/persons.csv: output/emails.csv
output/aliases.csv: output/emails.csv
output/emailRecipients.csv: output/emails.csv
emails: output/emails.csv

output/people.csv: output/emails.csv input/HRCEMAIL_names.csv
	python scripts/people.py   

working/noHeader/emails.csv: output/emails.csv
	mkdir -p working/noHeader
	tail +2 $^ > $@

working/noHeader/persons.csv: output/persons.csv
	mkdir -p working/noHeader
	tail +2 $^ > $@

working/noHeader/aliases.csv: output/aliases.csv
	mkdir -p working/noHeader
	tail +2 $^ > $@

working/noHeader/emailRecipients.csv: output/emailRecipients.csv
	mkdir -p working/noHeader
	tail +2 $^ > $@

output/database.sqlite: working/noHeader/emails.csv working/noHeader/persons.csv working/noHeader/aliases.csv working/noHeader/emailRecipients.csv
	-rm output/database.sqlite
	sqlite3 -echo $@ < scripts/sqliteImport.sql

sqlite: output/database.sqlite

all: emails sqlite

clean:
	rm -rf working
	rm -rf output
