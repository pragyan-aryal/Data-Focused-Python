import sys
import os
import glob
import shutil

# import modules
from Modules.indeed_platform import fetch_indeed_job
from Modules.indeed_platform import merge_jobs
from Modules.indeed_platform import fetch_job_description
from Modules.indeed_platform import merge_job_description
from Modules.indeed_platform import merge_data
from Modules.indeed_platform import get_location
from Modules.indeed_platform import salary
from Modules.indeed_platform import extract_skills

from Modules.h1b import get_h1b

from Modules.usa_jobs import get_usa_jobs, combine_data

from streamlit.web import cli as stcli

#Start of the app
print('Welcome to Career Compass')
print('\n')
print('You have 3 options to use this application')
print('1.: Scrape the Fresh Data (It will pull data for 10 different job titles) (Time Taken: 24 hrs +)')
print('2.: Scrape the Sample Data (It will pull limited data and visualize for 1 job title) (Time Taken: 5-10 minutes)')
print('3.: Continue with the existing data - this visualizes for all 10 job titles')

print('\n')
user_option = input('Enter the option you want to go with(1, 2, 3): ')

options = ["1", "2", "3"]

while user_option not in options:
    user_option = input("Please Enter the correct choice number(1, 2, 3): ")


# Looping for each choice
if user_option == "1":
    files = glob.glob('Final_Data/All/*')
    for f in files:
        os.remove(f)

    files = glob.glob('Final_Data/Final/*')
    for f in files:
        os.remove(f)

    jo = ['SE', 'PM', 'PJM', 'DA', 'DE', 'ME', 'CE', 'CAE', 'FEA', 'BA']

    # Fetch all indeed data
    fetch_indeed_job.fetch_job(sample="All")
    # Merge indeed data
    merge_jobs.merge_job([jo], "All")
    # get description for indeed data
    fetch_job_description.fetch_description([jo], sample="All")
    # Merge description with job data (done to isolate scraping tasks)
    merge_job_description.merge_data_description([jo], sample="All")
    # Merge all indeed data
    merge_data.merge_data([jo], sample="All")
    
    # get locations from API call, clean and merge with indeed data
    get_location.get_clean_location(sample="All")
    get_location.fetch_geo_loc(sample="All")
    get_location.merge_location(sample="All")

    # Clean salary and add new columns to data
    salary.clean_salary(sample="All")

    # Extract skills through regex for dashboard
    extract_skills.extract_skills(sample="All")

    # get H1B sponsors data through API
    get_h1b.h1b_scrape(sample="All")

    # Scrape and combine USA jobs Data
    get_usa_jobs.get_jobs(sample="All")
    combine_data.combine_data(sample="All")

    shutil.copy2('Final_Data/All/merged.parquet', 'Final_Data/Final/merged.parquet')
    shutil.copy2('Final_Data/All/h1_grader_data.tsv', 'Final_Data/Final/h1_grader_data.tsv')
    shutil.copy2('Final_Data/All/all_skills.tsv', 'Final_Data/Final/all_skills.tsv')
    shutil.copy2('Final_Data/All/USA_JOBS.csv', 'Final_Data/Final/USA_JOBS.csv')

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

    files = glob.glob('Final_Data/Sample/*')
    for f in files:
        os.remove(f)

    files = glob.glob('Final_Data/Final/*')
    for f in files:
        os.remove(f)

    # Fetch limited indeed data as a sample
    fetch_indeed_job.fetch_job([(job, jo)], exp, sample="Sample")
    # Merge indeed data
    merge_jobs.merge_job([jo], "Sample")
    # get description for indeed data
    fetch_job_description.fetch_description([jo], sample="Sample")
    # Merge description with job data (done to isolate scraping tasks)
    merge_job_description.merge_data_description([jo], sample="Sample")
    # Merge the indeed data
    merge_data.merge_data([jo], sample="Sample")

    # get locations from API call, clean and merge with indeed data
    get_location.get_clean_location(sample="Sample")
    get_location.fetch_geo_loc(sample="Sample")
    get_location.merge_location(sample="Sample")

    # Clean salary and add new columns to data
    salary.clean_salary(sample="Sample")

    # Extract skills through regex for dashboard
    extract_skills.extract_skills(sample="Sample")

    # get H1B sponsors data through API
    get_h1b.h1b_scrape([(job, jo)], sample="Sample")

    # Scrape and combine USA jobs Data
    get_usa_jobs.get_jobs([job], sample="Sample")
    combine_data.combine_data(sample="Sample")

    shutil.copy2('Final_Data/Sample/merged.parquet', 'Final_Data/Final/merged.parquet')
    shutil.copy2('Final_Data/Sample/h1_grader_data.tsv', 'Final_Data/Final/h1_grader_data.tsv')
    shutil.copy2('Final_Data/Sample/all_skills.tsv', 'Final_Data/Final/all_skills.tsv')
    shutil.copy2('Final_Data/Sample/USA_JOBS.csv', 'Final_Data/Final/USA_JOBS.csv')

else:
    files = glob.glob('Final_Data/Final/*')
    for f in files:
        os.remove(f)

    shutil.copy2('Final_Data/Existing/Indeed_Data.parquet', 'Final_Data/Final/merged.parquet')
    shutil.copy2('Final_Data/Existing/h1_grader_data.tsv', 'Final_Data/Final/h1_grader_data.tsv')
    shutil.copy2('Final_Data/Existing/all_skills.tsv', 'Final_Data/Final/all_skills.tsv')
    shutil.copy2('Final_Data/Existing/USA_Jobs_Data.csv', 'Final_Data/Final/USA_JOBS.csv')


sys.argv = ["streamlit", "run", "1_Career_Compass.py"]

sys.exit(stcli.main())
