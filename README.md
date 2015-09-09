# hillary-clinton-emails

This repo contains code to transform Hillary's emails from raw PDF documents to a SQLite database.

# Extracted data

There's two main files this produces, both in the output directory.

## [emails.csv](https://github.com/benhamner/hillary-clinton-emails/blob/master/output/emails.csv)

This file currently contains the following fields:

 - *SourceMonth* - month the email was released
 - *SourceFile* - zip file containing the email PDF
 - *FromRaw* - raw text of the extracted FROM address field
 - *ToRaw* - raw text of the extracted TO address field
 - *CcRaw* - raw text of the extracted CC address field
 - *DateSent* - raw text of the extracted Date address field
 - *Subject* - raw text of the extracted Subject
 - *CaseNumber* - FOIA case number
 - *DocNumber* - FOIA document number
 - *DateReleased* - date the document was released
 - *ReleaseInPartOrFull* - "RELEASE IN PART", "RELEASE IN FULL" or "UNKNOWN"
 - *RawText* - raw text extracted from the PDF via pdftotext

## [database.sqlite](https://github.com/benhamner/hillary-clinton-emails/blob/master/output/database.sqlite)

This SQLite database contains the Emails table, with the corresponding fields from emails.csv.

# Contributing: next steps

 - Improve the From/To address extraction mechanisms
 - Normalize various email address representations to people
 - Create People.csv, From.csv, To.csv, Cc.csv tables

# Running the download and extraction code

Running `make all` in the root directory will download the data and create emails.csv as well as database.sqlite, assuming you have all the requirements installed.

# Requirements

 - python3
 - pdftotext (utility to transform a PDF document to text)
 - GNU make
 - sqlite3
