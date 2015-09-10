import numpy as np 
import pandas as pd 

def normalize_address(raw_address):
    for c in ["'", ",", "°", "•", "`", '"', "‘", "-"]:
        raw_address = raw_address.replace(c, "")
    raw_address = raw_address.lower()
    if "<" in raw_address:
        prefix = raw_address[:raw_address.index("<")].strip()
        if prefix:
            return prefix
    return raw_address.strip()

emails = pd.read_csv("input/emailsNoId.csv")
emails["MetadataTo"].replace(np.nan, "", inplace=True)
emails["ExtractedTo"].replace(np.nan, "", inplace=True)
emails["MetadataFrom"].replace(np.nan, "", inplace=True)
emails["ExtractedFrom"].replace(np.nan, "", inplace=True)
emails.sort(columns=["DocNumber"], inplace=True)
emails.insert(0, "Id", list(range(1, len(emails)+1)))
emails.insert(5, "SenderPersonId", np.nan)

alias_person = pd.read_csv("versionedInput/alias_person.csv")
alias_person["AliasName"] = [normalize_address(alias) for alias in alias_person["AliasName"]]

persons = pd.DataFrame(columns=["Id", "Name"])
aliases = pd.DataFrame(columns=["Id", "Alias", "PersonId"])
email_receivers = pd.DataFrame(columns=["Id", "EmailId", "PersonId"]).astype(int)

def add_alias(aliases, persons, alias_name, person_name):
    if len(np.where(aliases["Alias"]==alias_name)[0])>0:
        return
    locs = np.where(persons["Name"]==person_name)[0]
    if len(locs)>0:
        person_id = persons["Id"][locs[0]]
    else:
        person_id = len(persons)+1
        persons.loc[person_id-1] = [person_id, person_name]
    alias_id = len(aliases)+1
    aliases.loc[alias_id-1] = [alias_id, alias_name.lower(), person_id]

for (i, alias_person) in alias_person.iterrows():
    add_alias(aliases, persons, alias_person["AliasName"], alias_person["PersonName"])

log = open("working/outputCsvsLog.txt", "w")

for (i, email) in emails.iterrows():
    from_person_id = None
    from_address = normalize_address(email["MetadataFrom"].split(";")[0])
    if from_address != "":
        locs = np.where(aliases["Alias"]==from_address)[0]
        if len(locs)==0:
            add_alias(aliases, persons, from_address, from_address)
            log.write("Added From Person: %s\n" % from_address)
        loc = np.where(aliases["Alias"]==from_address)[0][0]
        from_person_id = aliases["PersonId"][loc]
        from_person_name = persons["Name"][from_person_id-1]
        emails.loc[i, "SenderPersonId"] = from_person_id
        if email["ExtractedFrom"] != "":
            add_alias(aliases, persons, normalize_address(email["ExtractedFrom"]), from_person_name)
    to_addresses = email["MetadataTo"].split(";") + email["ExtractedTo"].split(";")
    to_addresses = sorted(list(set([normalize_address(x) for x in to_addresses])))
    if "" in to_addresses:
        to_addresses.remove("")
    for to_address in to_addresses:
        locs = np.where(aliases["Alias"]==to_address)[0]
        if len(locs)==0:
            add_alias(aliases, persons, to_address, to_address)
            log.write("Added To Person: %s\n" % to_address)
        loc = np.where(aliases["Alias"]==to_address)[0][0]
        # don't add a receiver if they were also the sender
        if from_person_id != aliases["PersonId"][loc]:
            email_receivers.loc[len(email_receivers)] = [len(email_receivers)+1, email["Id"], aliases["PersonId"][loc]]

persons.to_csv("output/Persons.csv", index=False)
aliases.to_csv("output/Aliases.csv", index=False)
emails.to_csv("output/Emails.csv", index=False, float_format="%0.0f")
email_receivers.to_csv("output/EmailReceivers.csv", index=False, float_format="%0.0f")

log.close()