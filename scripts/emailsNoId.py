import arrow
import csv
import os
import numpy as np
import pandas as pd
import re
from subprocess import call

def extract_release_type(raw_text):
    if re.search(r"RELEASE\s+IN\s+PART", raw_text):
        return "RELEASE IN PART"
    if re.search(r"RELEASE\s+IN\s+FULL", raw_text):
        return "RELEASE IN FULL"
    return "UNKNOWN" 

def extract_field(regex, raw_text):
    m=re.search(regex, raw_text)
    if m:
        return m.groups()[0].strip()
    return ""

def metadata_timestamp_to_string(timestamp):
    if np.isnan(timestamp):
        return ""
    return str(arrow.get(timestamp/1000))

metadata = pd.read_csv("input/metadata.csv")
metadata["DocNumber"] = [os.path.splitext(os.path.split(pdf_link)[1])[0] for pdf_link in metadata["pdfLink"]]

f = open("input/emailsNoId.csv", "w")
writer = csv.writer(f)
writer.writerow(["DocNumber",
                 "MetadataSubject",
                 "MetadataTo",
                 "MetadataFrom",
                 "MetadataDateSent",
                 "MetadataDateReleased",
                 "MetadataPdfLink",
                 "MetadataCaseNumber",
                 "MetadataDocumentClass",
                 "ExtractedSubject",
                 "ExtractedTo",
                 "ExtractedFrom",
                 "ExtractedCc",
                 "ExtractedDateSent",
                 "ExtractedCaseNumber",
                 "ExtractedDocNumber",
                 "ExtractedDateReleased",
                 "ExtractedReleaseInPartOrFull",
                 "RawText"])

for subdir, dirs, files in os.walk("working/text"):
    if subdir=="working/text":
        continue
    for filename in files:
        doc_number = os.path.splitext(filename)[0]
        locs = np.where(metadata["DocNumber"]==doc_number)[0]
        if len(locs) != 1:
            raise Exception("There isn't exactly one matching filename for %s: %s" % (filename, locs))
        loc = locs[0]
        filepath = os.path.join(subdir, filename)
        raw_text = open(filepath).read()
        writer.writerow([doc_number,
                         metadata["subject"][loc],
                         metadata["to"][loc],
                         metadata["from"][loc],
                         metadata_timestamp_to_string(metadata["docDate"][loc]),
                         metadata_timestamp_to_string(metadata["postedDate"][loc]),
                         metadata["pdfLink"][loc],
                         metadata["caseNumber"][loc],
                         metadata["documentClass"][loc],
                         extract_field(r"Subject:(.*?)\n", raw_text),
                         extract_field(r"To:(.*?)\n", raw_text),
                         extract_field(r"From:(.*?)\n", raw_text),
                         extract_field(r"Cc:(.*?)\n", raw_text),
                         extract_field(r"Sent:(.*?)\n", raw_text),
                         extract_field(r"Case No. (.+?-\d+-\d+)", raw_text),
                         extract_field(r"Doc No. (.\d+)", raw_text),
                         extract_field(r"Date: (\d\d/\d\d/\d\d\d\d)", raw_text),
                         extract_release_type(raw_text),
                         raw_text])

f.close()
