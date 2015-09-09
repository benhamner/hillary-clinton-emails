.separator ","

CREATE TABLE Emails (
    SourceMonth TEXT,
    SourceFile TEXT,
    FromRaw TEXT,
    ToRaw TEXT,
    CcRaw TEXT,
    DateSent TEXT,
    Subject TEXT,
    CaseNumber TEXT,
    DocNumber TEXT,
    DateReleased TEXT,
    ReleaseInPartOrFull TEXT,
    RawText TEXT);

.import "working/emailsNoHeader.csv" Emails

CREATE INDEX emails_docnumber_ix ON Emails (DocNumber);
