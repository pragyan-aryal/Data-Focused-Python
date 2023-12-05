import json
import http.client
import csv

#fetching data through API
conn = http.client.HTTPSConnection("h1bgrader.com")

headersList = {
 "Accept": "/",
 "User-Agent": "Thunder Client (https://www.thunderclient.com)",
 "Content-Type": "application/x-www-form-urlencoded" 
}

jobs = {'BA': 'Business Analyst', 'DA': 'Data Analyst', 'DE': 'Data Engineer', 'PM': 'Product Manager', 'PJM': 'Project Manager', 'FEA' : 'FEA Engineer', 'SE': 'Software Engineer', 'ME': 'Mechanical Engineer', 'CE': 'Civil Engineer', 'CAE': 'CAE Engineer'}
     
payload = "draw=1&start=0&length=1000&job={}"

total_data = []

for job_code, job in jobs.items():    
    conn.request("POST", "/api/listby", payload.format(job), headersList)
    response = conn.getresponse()
    result = response.read()

    outer_data = json.loads(result) 
    inner_data = outer_data['data']

    for i in inner_data:
        i['category_code'] = job_code
        total_data.append(i)

keys = list(total_data[0].keys()) + ['category_code']

with open('h1_grader_data.tsv', 'w', newline='') as f:
    writer = csv.writer(f, delimiter='\t')

    writer.writerow(keys)

    for row in total_data:
        writer.writerow(row.values())

