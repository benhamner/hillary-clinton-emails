import os
from subprocess import call

for subdir, dirs, files in os.walk("working/pdfs"):
    if subdir=="working/pdfs":
        continue
    newdir = os.path.join("working/rawText", os.path.split(subdir)[1])
    if not os.path.exists(newdir):
        call(["mkdir", newdir])
    for filename in files:
        filepath = os.path.join(subdir, filename)
        if not filepath.endswith(".pdf"):
            raise Exception("Unexpected file path: %s" % os.path.join(subdir, filename))
        call(["pdftotext", 
              "-raw",
              os.path.join(subdir, filename),
              os.path.join(newdir, os.path.splitext(filename)[0]+".txt")])
