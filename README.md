# CareerCompass
CareerCompass is a Python-based innovative application designed to empower job seekers with detailed insights on job skills, salary, sponsorship, and opportunities.  
This application currrently uses websites such as Indeed, USAJobs, H1BGrader, and PositionStack.

## Installation

1. First ensure that these packages are installed for smooth running of the application.

numpy, requests = 2.31.0, beautifulsoup4 = 4.12.0, matplotlib = 3.7.1, streamlit = 1.27.2, altair, pandas = 1.5.3, st_pages, plotly = 5.18.0, DrissionPage = 4.0.0b14, selenium = 4.15.2, plotly, wordcloud

```
pip install -r requirements.txt
```
2. All the paths of the CSV, TSV, Parquet files and images used in the code are relative. This means that all the files should work as they are in the same folder.
path addresses of that file on the system it is being installed on.

3. Run the file named "app.py" in the folder. Consequent python files are run from this source code only.

```
python app.py
```

## Features
This application currenlty offers three options to display information to the user:

- [Scrape Live Data](#scrape-live-data)

- [Scrape Sample Data](#scrape-sample-data)

- [Work with Existing Data](#work-with-existing-data)

### Scrape Live Data
Scraping live data from all the four live websites will take more than 24 hours. This scrapes relevant information of all 10 job titles. However, this is not recommended to users.
### Scrape Sample Data
This option is to scrape sample data and visualize for a specific job title, chosen by the user. This will take 5~10 minutes. 
### Work with Existing Data
This option runs the program with the existing data and shows the visualizations for all the 10 job titles.

## Streamlit

Using streamlit, an interactive dashboard is made for customers to
- Instantly discover requisite skills for specific job roles
- Identify number of companies offering H1B sponsorships
- Explore salary dynamics for various job titles
- Understand evolving job and location trends.

Please visit- https://career-compass.streamlit.app/ to interact with CareerCompass.

## Working 
Indeed and USAjobs are the primary websites from which data has been scraped. Additionally, H1B grader and PositionStack(GeoLocations) websites are used for API response.

## Limitations

This application currently has a limited number of job titles on its database as currently very few websites allow scraping.

Additionally, the website doesn't contain an exhaustive list of skills and companies information. 

## Authors
1. Amogh Borikar (aborikar@andrew.cmu.edu)
2. Ankita Bodigam (abodigam@andrew.cmu.edu)
3. Pragyan Aryal (paryal@andrew.cmu.edu)
4. Prakhar Sharma (prakhars@andrew.cmu.edu)

## More Information

For more information on how the code works, please visit- https://youtu.be/m0I8J0YYSLU?si=tAc3KkjCKx2fYOzC

## Appendix

The sites used for scraping information are:
- [Indeed.com](https://www.indeed.com/)
- [USAjobs](https://www.usajobs.gov/)
- [H1Bgrader.com](https://h1bgrader.com/)
- [PositionStack](https://positionstack.com/)