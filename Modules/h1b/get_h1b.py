import json
import http.client
import csv

jobs = [('Software Engineer', 'SE'), ('Data Engineer', 'DE'), ('Data Analyst', 'DA'), ('Mechanical Engineer', 'ME'),
      ('Business Analyst', 'BA'), ('Product Manager', 'PM'), ('Project Manager', 'PJM'), ('CAE Engineer', 'CAE'),
      ('FEA Engineer', 'FEA'), ('Civil Engineer', 'CE')]


def h1b_scrape(j1=jobs, sample="All"):
    # fetching data through API
    conn = http.client.HTTPSConnection("h1bgrader.com")

    headersList = {
        "Accept": "/",
        "User-Agent": "Thunder Client (https://www.thunderclient.com)",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    payload = "draw=1&start=0&length=1000&job={}"

    total_data = []

    for job, job_code in j1:
        conn.request("POST", "/api/listby", payload.format(job), headersList)
        response = conn.getresponse()
        result = response.read()

        outer_data = json.loads(result)
        inner_data = outer_data['data']

        for i in inner_data:
            i['category_code'] = job_code
            total_data.append(i)

    keys = list(total_data[0].keys()) + ['category_code']

    with open('Final_Data/' + sample + '/h1_grader_data.tsv', 'w', newline='') as f:
        writer = csv.writer(f, delimiter='\t')

        writer.writerow(keys)

        for row in total_data:
            writer.writerow(row.values())
