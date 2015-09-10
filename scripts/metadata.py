import csv
import json
import re
import requests

response = requests.get("https://foia.state.gov/searchapp/Search/SubmitSimpleQuery",    
    params = {"searchText": "*",
              "beginDate": "false",
              "endDate": "false",
              "collectionMatch": "Clinton_Email",
              "postedBeginDate": "false",
              "postedEndDate": "false",
              "caseNumber": "false",
              "page": 1,
              "start": 0,
              "limit": 100000},
    verify=False)

return_json = re.sub(r'new Date\(([0-9]{1,})\)',r'\1',response.text)
return_json = re.sub(r'new ?Date\((-[0-9]{1,})\)',r'null',return_json)

data = json.loads(return_json)
header = list(data["Results"][0].keys())
print(header)

f = open("input/metadata.csv", "w")
writer = csv.writer(f)
writer.writerow(header)

for row in data["Results"]:
    writer.writerow([row[col] for col in header])

f.close()
