import numpy as np 
import pandas as pd 

emails = pd.read_csv("output/emails.csv")
emails["MetadataTo"].replace(np.nan, "", inplace=True)
emails["ExtractedTo"].replace(np.nan, "", inplace=True)
emails["MetadataFrom"].replace(np.nan, "", inplace=True)
emails["ExtractedFrom"].replace(np.nan, "", inplace=True)

raw_persons = pd.read_csv("input/HRCEMAIL_names.csv")[1:]

persons = pd.DataFrame(columns=["Id", "Name"])
aliases = pd.DataFrame(columns=["Id", "Alias", "PersonId"])
emails_from_persons = pd.DataFrame(columns=["Id", "EmailId", "PersonId"])
emails_to_persons = pd.DataFrame(columns=["Id", "EmailId", "PersonId"])

for (i, raw_person) in raw_persons.iterrows():
    locs = np.where(persons["Name"]==raw_person["commonName"])[0]
    if len(locs)>0:
        person_id = persons["Id"][locs[0]]
    else:
        person_id = len(persons)+1
        persons.loc[person_id-1] = [person_id, raw_person["commonName"]]
    alias_id = len(aliases)+1
    aliases.loc[alias_id-1] = [alias_id, raw_person["originalName"], person_id]

for (i, email) in emails.iterrows():
    if email["MetadataFrom"] != "":
        from_locs = np.where(aliases["Alias"]==email["MetadataFrom"])[0]
        if len(from_locs)==0:
            print(email["MetadataFrom"])

#    print("MetadataTo:  %s" % email["MetadataTo"])
#    print("ExtractedTo: %s" % email["ExtractedTo"])
#    print([x.strip() for x in email["ExtractedTo"].split(";")])
#    print("MetadataFrom:  %s" % email["MetadataFrom"])
#    print("ExtractedFrom: %s" % email["ExtractedFrom"])
#    wait = input("Press Enter to Continue")

#extracted_to = [address.strip() for to_field in emails["ExtractedTo"] for address in to_field.split(";")]
#print(len(extracted_to))
#print(len(set(extracted_to)))
#print((emails["ExtractedTo"]!="").sum())


