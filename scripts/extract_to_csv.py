import csv
import os
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

def extract_features(raw_text):
    return {
        "FromRaw": extract_field(r"From:(.*?)\n", raw_text),
        "ToRaw": extract_field(r"To:(.*?)\n", raw_text),
        "CcRaw": extract_field(r"Cc:(.*?)\n", raw_text),
        "DateSent": extract_field(r"Sent:(.*?)\n", raw_text),
        "Subject": extract_field(r"Subject:(.*?)\n", raw_text),
        "CaseNumber": extract_field(r"Case No. (.+?-\d+-\d+)", raw_text),
        "DocNumber": extract_field(r"Doc No. (.\d+)", raw_text),
        "DateReleased": extract_field(r"Date: (\d\d/\d\d/\d\d\d\d)", raw_text),
        "ReleaseInPartOrFull": extract_release_type(raw_text)
    }

f = open("output/emails.csv", "w")
writer = csv.writer(f)
writer.writerow(["SourceMonth",
                 "SourceFile",
                 "FromRaw",
                 "ToRaw",
                 "CcRaw",
                 "DateSent",
                 "Subject",
                 "CaseNumber",
                 "DocNumber",
                 "DateReleased",
                 "ReleaseInPartOrFull",
                 "RawText"])

for subdir, dirs, files in os.walk("working/text"):
    if subdir=="working/text":
        continue
    month = os.path.split(subdir)[1]
    for filename in files:
        filepath = os.path.join(subdir, filename)
        raw_text = open(filepath).read()
        features = extract_features(raw_text)
        writer.writerow([month,
                         os.path.splitext(filename)[0]+".pdf",  
                         features["FromRaw"],
                         features["ToRaw"],
                         features["CcRaw"],
                         features["DateSent"],
                         features["Subject"],
                         features["CaseNumber"],
                         features["DocNumber"],
                         features["DateReleased"],
                         features["ReleaseInPartOrFull"],
                         raw_text])

f.close()
