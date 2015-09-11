# hillary-clinton-emails

*This is a work in progress - any help normalizing and extracting this data's much appreciated!*

This repo contains code to transform [Hillary Clinton's emails released through the FOIA request](https://foia.state.gov/Search/Results.aspx?collection=Clinton_Email) from raw PDF documents to CSV files and a SQLite database, making it easier to understand and analyze the documents.

**[A zip of the extracted data is available for download on Kaggle](https://www.kaggle.com/c/hillary-clinton-emails/data)**.

Check out some analytics on this data on **[Kaggle Scripts](https://www.kaggle.com/c/hillary-clinton-emails/scripts)**.

Note that conversion is very imprecise: there's plenty of room to improve the PDF conversion, the sender/receiver extraction, and the body text extraction.

# Extracted data

There are five main output files this produces: four CSV files and one SQLite database.

Note that each table contains a numeric `Id` column. This `Id` column is only meant to be used to join the tables: it is internally consistent, but each entity may have a different `Id` when the data's updated.

## Emails.csv

This file currently contains the following fields:

 - **Id** - unique identifier for internal reference
 - **DocNumber** - FOIA document number
 - **MetadataSubject** - Email SUBJECT field (from the FOIA metadata)
 - **MetadataTo** - Email TO field (from the FOIA metadata)
 - **MetadataFrom** - Email FROM field (from the FOIA metadata)
 - **SenderPersonId** - PersonId of the email sender (linking to Persons table)
 - **MetadataDateSent** - Date the email was sent (from the FOIA metadata)
 - **MetadataDateReleased** - Date the email was released (from the FOIA metadata)
 - **MetadataPdfLink** - Link to the original PDF document (from the FOIA metadata)
 - **MetadataCaseNumber** - Case number (from the FOIA metadata)
 - **MetadataDocumentClass** - Document class (from the FOIA metadata)
 - **ExtractedSubject** - Email SUBJECT field (extracted from the PDF)
 - **ExtractedTo** - Email TO field (extracted from the PDF)
 - **ExtractedFrom** - Email FROM field (extracted from the PDF)
 - **ExtractedCc** - Email CC field (extracted from the PDF)
 - **ExtractedDateSent** - Date the email was sent (extracted from the PDF)
 - **ExtractedCaseNumber** - Case number (extracted from the PDF)
 - **ExtractedDocNumber** - Doc number (extracted from the PDF)
 - **ExtractedDateReleased** - Date the email was released (extracted from the PDF)
 - **ExtractedReleaseInPartOrFull** - Whether the email was partially censored (extracted from the PDF)
 - **ExtractedBodyText** - Attempt to only pull out the text in the body that the email sender wrote (extracted from the PDF)
 - **RawText** - Raw email text (extracted from the PDF)

## Persons.csv

 - **Id** - unique identifier for internal reference
 - **Name** - person's name

## Aliases.csv

 - **Id** - unique identifier for internal reference
 - **Alias** - text in the From/To email fields that refers to the person
 - **PersonId** - person that the alias refers to

## EmailReceivers.csv

 - **Id** - unique identifier for internal reference
 - **EmailId** - Id of the email
 - **PersonId** - Id of the person that received the email

## database.sqlite

This SQLite database contains all of the above tables (Emails, Persons, Aliases, and EmailReceivers) with their corresponding fields. You can see the schema and ingest code under [scripts/sqlImport.sql](https://github.com/benhamner/hillary-clinton-emails/blob/master/scripts/sqliteImport.sql)

# Contributing: next steps

 - Improve the From/To address extraction mechanisms
 - Normalize various email address representations to people
 - Improve the BodyText extraction

# Running the download and extraction code

Running `make all` in the root directory will download the data (~162mb total) and create the output files, assuming you have all the requirements installed.

# Requirements

*This has only been tested on OS X, it may or may not work on other operating systems.*

 - python3
   - pandas
   - arrow
   - numpy
 - pdftotext (utility to transform a PDF document to text)
 - GNU make
 - sqlite3

# References

The source PDF documents for this repo were downlaoded from the [WSJ Clinton Inbox search](http://graphics.wsj.com/hillary-clinton-email-documents/).

I created this project before I realized the WSJ also open-sourced some code they used to create the Inbox Search. Subsequently, I've included some material from their open source project as well: I used their [HRCEMAIL_names.csv](https://raw.githubusercontent.com/wsjdata/clinton-email-cruncher/d8dc1916465b90e4147460f9e432cf9cafc8d3b5/HRCEMAIL_names.csv) to seed [alias_person.csv](https://github.com/benhamner/hillary-clinton-emails/blob/master/versionedInput/alias_person.csv). I also scraped metadata from foia.state.gov in a similar fashion as they did in [downloadMetadata.py](https://github.com/wsjdata/clinton-email-cruncher/blob/master/downloadMetadata.py).