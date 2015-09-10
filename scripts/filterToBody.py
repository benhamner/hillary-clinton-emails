import os
import re
from subprocess import call

num_files = 0
num_from  = 0
num_subj  = 0

def filter_body(text):
    text = re.sub(r"(\n|^)UNCLASSIFIED.*", "", text)
    text = re.sub(r"(\n|^)CONFIDENTIAL.*", "", text)
    text = re.sub(r"(\n|^)Classified by.*", "", text)
    return text

def extract_body(raw_text):
    m = re.search(r"\nSubject.*?\n(.*?)(Original Message|From:)", raw_text, re.DOTALL)
    if m:
        return filter_body(m.groups()[0])
    m = re.search(r"\nSubject.*?\n(.+)", raw_text, re.DOTALL)
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
        num_files += 1
        if "From:" in raw_text:
            num_from += 1
        if "Subject:" in raw_text:
            num_subj += 1

print(num_files)
print(num_from)
print(num_subj)