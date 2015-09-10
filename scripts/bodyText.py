import os
import re
from subprocess import call

def filter_body(text):
    patterns = [r"\x0c",
                r"(\n|^)UNCLASSIFIED.*",
                r"(\n|^)CONFIDENTIAL.*",
                r"(\n|^)Classified by.*",
                r"(\n|^)Attachments:.*"]
    for repeat in range(3):
        for pattern in patterns:
            text = re.sub(pattern, "", text)
    return text.strip()

def extract_body(raw_text):
    m = re.search(r"\nSubject.*?\n(.*?)(Original Message|From:)", raw_text, re.DOTALL)
    if m:
        return filter_body(m.groups()[0])
    m = re.search(r"\nSubject.*?\n(.+)", raw_text, re.DOTALL)
    if m:
        return filter_body(m.groups()[0])
    m = re.search(r"\nTo:.*?\n(.*?)(Original Message|From:)", raw_text, re.DOTALL)
    if m:
        return filter_body(m.groups()[0])
    m = re.search(r"\nTo:.*?\n(.+)", raw_text, re.DOTALL)
    if m:
        return filter_body(m.groups()[0])
    return ""

for subdir, dirs, files in os.walk("working/rawText"):
    if subdir=="working/rawText":
        continue
    newdir = os.path.join("working/bodyText", os.path.split(subdir)[1])
    if not os.path.exists(newdir):
        call(["mkdir", "-p", newdir])
    for filename in files:
        input_file = os.path.join(subdir, filename)
        output_file = os.path.join(newdir, filename)
        if not input_file.endswith(".txt"):
            raise Exception("Unexpected file path: %s" % os.path.join(subdir, filename))
        raw_text = open(input_file).read()
        f = open(output_file, "w")
        f.write(extract_body(raw_text))
        f.close()
