import csv
import os
import re
from subprocess import call

def extract_release_type(raw_text):
    if "RELEASE IN PART" in raw_text:
        return "RELEASE IN PART"
    if "RELEASE IN FULL" in raw_text:
        return "RELEASE IN FULL"
    return "UNKNOWN" 

def extract_field(regex, raw_text):
    m=re.search(regex, raw_text)
    if m:
        return m.groups()[0].strip()
    return ""

def extract_features(raw_text):
    return {
        "From": extract_field(r"From:(.*?)\n", raw_text),
        "To": extract_field(r"To:(.*?)\n", raw_text),
        "Cc": extract_field(r"Cc:(.*?)\n", raw_text),
        "DateSent": extract_field(r"Sent:(.*?)\n", raw_text),
        "Subject": extract_field(r"Subject:(.*?)\n", raw_text),
        "ReleaseInPartOrFull": extract_release_type(raw_text)
    }

f = open("working/emails.csv", "w")
writer = csv.writer(f)
writer.writerow(["SourceMonth",
                 "SourceFile",
                 "From",
                 "To",
                 "Cc",
                 "DateSent",
                 "Subject",
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
                         features["From"],
                         features["To"],
                         features["Cc"],
                         features["DateSent"],
                         features["Subject"],
                         features["ReleaseInPartOrFull"],
                         raw_text])

f.close()
