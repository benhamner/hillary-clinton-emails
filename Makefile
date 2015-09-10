
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

working/rawText/.sentinel: working/pdfs/.sentinel
	mkdir -p working/rawText
	python scripts/pdfToRawText.py
	touch working/rawText/.sentinel

working/bodyText/.sentinel: working/rawText/.sentinel
	mkdir -p working/bodyText
	python scripts/bodyText.py
	touch working/bodyText/.sentinel
text: working/bodyText/.sentinel

input/emailsNoId.csv: working/rawText/.sentinel working/bodyText/.sentinel input/metadata.csv
	python scripts/emailsNoId.py

output/Emails.csv: input/emailsNoId.csv
	mkdir -p output
	python scripts/outputCsvs.py
output/Persons.csv: output/Emails.csv
output/Aliases.csv: output/Emails.csv
output/EmailRecipients.csv: output/Emails.csv
csv: output/Emails.csv output/Persons.csv output/Aliases.csv output/EmailRecipients.csv

working/noHeader/Emails.csv: output/Emails.csv
	mkdir -p working/noHeader
	tail +2 $^ > $@

working/noHeader/Persons.csv: output/Persons.csv
	mkdir -p working/noHeader
	tail +2 $^ > $@

working/noHeader/Aliases.csv: output/Aliases.csv
	mkdir -p working/noHeader
	tail +2 $^ > $@

working/noHeader/EmailRecipients.csv: output/EmailRecipients.csv
	mkdir -p working/noHeader
	tail +2 $^ > $@

output/database.sqlite: working/noHeader/Emails.csv working/noHeader/Persons.csv working/noHeader/Aliases.csv working/noHeader/EmailRecipients.csv
	-rm output/database.sqlite
	sqlite3 -echo $@ < scripts/sqliteImport.sql

sqlite: output/database.sqlite

all: csv sqlite

clean:
	rm -rf working
	rm -rf output
