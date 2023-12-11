import sys

from Modules.indeed_platform import fetch_indeed_job
from Modules.indeed_platform import merge_jobs
from Modules.indeed_platform import fetch_job_description
from Modules.indeed_platform import merge_job_description
from Modules.indeed_platform import merge_data
from Modules.indeed_platform import get_location
from Modules.indeed_platform import salary

from streamlit.web import cli as stcli

print('Welcome to Career Compass')
print('\n')
print('You have 3 option to use this application')
print('1.: Scrape the Fresh Data (It will pull 10 different job titles data) (Time Taken: )')
print('2.: Scrape the Sample Data (It will pull limited data for 1 job title) (Time Taken: 30 minute)')
print('3.: Continue with the existing data')

print('\n')
user_option = input('Enter the option you want to go with(1, 2, 3): ')

options = ["1", "2", "3"]

while user_option not in options:
    user_option = input("Please Enter the correct choice number(1, 2, 3): ")

if user_option == "1":
    pass
elif user_option == "2":
    match = False
    job = ""
    j_ = ["Software Engineer", "Data Analyst", "Product Manager", "Project Manager", "Business Analyst",
          "Data Engineer", "Mechanical Engineer", "CAE Engineer", "FEA Engineer", "Civil Engineer"]
    j_oc = ["SE", "DA", "PM", "PJM", "BA", "DE", "ME", "CAE", "FEA", "CE"]

    expl_lvl = ["ENTRY_LEVEL", "MID_LEVEL", "SENIOR_LEVEL", ""]

    while job not in j_:
        job = input("\nPlease Select the job title From this list (Software Engineer, Data Analyst, Product Manager, "
                    "Project Manager, Business Analyst, Data Engineer, Mechanical Engineer, CAE Engineer, "
                    "FEA Engineer, Civil Engineer): ")

    print('\nData for all experience level will be scraped by default. If you want data for just one experience level '
          '(ENTRY_LEVEL, MID_LEVEL, SENIOR_LEVEL)')

    exp = input("\nEnter the experience level you want to scrape. If None default will be considered: ")

    while exp not in expl_lvl:
        exp = input("\nEnter the experience level you want to scrape. If None default will be considered: ")

    if exp == "":
        exp = expl_lvl[:3]
    else:
        exp =[exp]

    jo = j_oc[j_.index(job)]

    fetch_indeed_job.fetch_job([(job, jo)], exp, sample="Sample")

    merge_jobs.merge_job([jo], "Sample")

    fetch_job_description.fetch_description([jo], sample="Sample")

    merge_job_description.merge_data_description([jo], sample="Sample")

    merge_data.merge_data([jo], sample="Sample")

    get_location.get_clean_location(sample="Sample")

    get_location.fetch_geo_loc(sample="Sample")

    get_location.merge_location(sample="Sample")

    salary.clean_salary(sample="Sample")

    sys.argv = ["streamlit", "run", "1_Career_Compass.py"]
    sys.exit(stcli.main())

else:
    sys.argv = ["streamlit", "run", "1_Career_Compass.py"]
    sys.exit(stcli.main())