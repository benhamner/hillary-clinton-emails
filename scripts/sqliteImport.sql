.separator ","

CREATE TABLE Emails (
    Id INTEGER PRIMARY KEY,
    DocNumber TEXT,
    MetadataSubject TEXT,
    MetadataTo TEXT,
    MetadataFrom TEXT,
    FromPersonId INTEGER,
    MetadataDateSent TEXT,
    MetadataDateReleased TEXT,
    MetadataPdfLink TEXT,
    MetadataCaseNumber TEXT,
    MetadataDocumentClass TEXT,
    ExtractedSubject TEXT,
    ExtractedTo TEXT,
    ExtractedFrom TEXT,
    ExtractedCc TEXT,
    ExtractedDateSent TEXT,
    ExtractedCaseNumber TEXT,
    ExtractedDocNumber TEXT,
    ExtractedDateReleased TEXT,
    ExtractedReleaseInPartOrFull TEXT,
    RawText TEXT);

CREATE TABLE Persons (
    Id INTEGER PRIMARY KEY,
    Name TEXT);

CREATE TABLE Aliases (
    Id INTEGER PRIMARY KEY,
    Alias TEXT,
    PersonId INTEGER);

CREATE TABLE EmailRecipients (
    Id INTEGER PRIMARY KEY,
    EmailId INTEGER,
    PersonId INTEGER);

.import "working/noHeader/emails.csv" Emails
.import "working/noHeader/persons.csv" Persons
.import "working/noHeader/aliases.csv" Aliases
.import "working/noHeader/emailRecipients.csv" EmailRecipients

CREATE INDEX emails_frompersonid_ix ON Emails (FromPersonId);
CREATE INDEX emails_docnumber_ix ON Emails (DocNumber);

CREATE INDEX aliases_personid_ix ON Aliases (PersonId);

CREATE INDEX emailrecipients_emailid_ix ON EmailRecipients (EmailId);
CREATE INDEX emailrecipients_personid_ix ON EmailRecipients (PersonId);
