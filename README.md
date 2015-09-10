# hillary-clinton-emails

This repo contains code to transform Hillary's emails from raw PDF documents to a SQLite database.

This is a work in progress - any help normalizing and extracting this data's much appreciated!

# Extracted data

There's two main files this produces, both in the output directory.

## [emails.csv](https://github.com/benhamner/hillary-clinton-emails/blob/master/output/emails.csv)

This file is ~20mb and currently contains the following fields:

 - **SourceMonth** - month the email was released
 - **SourceFile** - zip file containing the email PDF
 - **FromRaw** - raw text of the extracted FROM address field
 - **ToRaw** - raw text of the extracted TO address field
 - **CcRaw** - raw text of the extracted CC address field
 - **DateSent** - raw text of the extracted Date address field
 - **Subject** - raw text of the extracted Subject
 - **CaseNumber** - FOIA case number
 - **DocNumber** - FOIA document number
 - **DateReleased** - date the document was released
 - **ReleaseInPartOrFull** - "RELEASE IN PART", "RELEASE IN FULL" or "UNKNOWN"
 - **RawText** - raw text extracted from the PDF via pdftotext

## [database.sqlite](https://github.com/benhamner/hillary-clinton-emails/blob/master/output/database.sqlite)

This ~20mb SQLite database contains the Emails table, with the corresponding fields from emails.csv.

# Contributing: next steps

 - Improve the From/To address extraction mechanisms
 - Normalize various email address representations to people
 - Create People.csv, From.csv, To.csv, Cc.csv tables

# Running the download and extraction code

Running `make all` in the root directory will download the data (~162mb total) and create emails.csv as well as database.sqlite, assuming you have all the requirements installed.

# Requirements

 - python3
 - pdftotext (utility to transform a PDF document to text)
 - GNU make
 - sqlite3

# References

The source PDF documents for this repo were downlaoded from the [WSJ Clinton Inbox search](http://graphics.wsj.com/hillary-clinton-email-documents/).

I created this project before I realized the WSJ also open-sourced some code they used to create the Inbox Search. Subsequently, I've included some material from their open source project as well: I used their [HRCEMAIL_names.csv](https://raw.githubusercontent.com/wsjdata/clinton-email-cruncher/d8dc1916465b90e4147460f9e432cf9cafc8d3b5/HRCEMAIL_names.csv) to seed [alias_person.csv](https://github.com/benhamner/hillary-clinton-emails/blob/master/output/versionedInput.csv). I also scraped metadata from foia.state.gov in a similar fashion as they did in [downloadMetadata.py](https://github.com/wsjdata/clinton-email-cruncher/blob/master/downloadMetadata.py).