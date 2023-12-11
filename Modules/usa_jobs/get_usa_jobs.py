from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import pandas as pd
import requests
from bs4 import BeautifulSoup


def get_jobs(sample="All"):
    def page_search_driver(job_title):
        # Set up Chrome options in headless mode
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Run Chrome in headless mode
        chrome_options.add_argument("--disable-gpu")  # Disable GPU acceleration

        # HTML url encoding for search
        job_title = job_title.replace(" ", "%20")

        search_url = "https://www.usajobs.gov/Search/Results?k=" + job_title

        # Create a Chrome webdriver instance with the specified options
        driver = webdriver.Chrome(options=chrome_options)

        try:
            # Navigate to the URL
            driver.get(search_url)

            # Wait for the page to fully load
            time.sleep(0.5)

            # Get the HTML content after dynamic loading
            html_content = driver.page_source

            # Close the browser window
            driver.quit()

            soup = BeautifulSoup(html_content, 'html.parser')

            # Find all the titles within the specified class
            page_listings = [li.a.get('title') for li in soup.find_all('li', class_='usajobs-search-pagination__page')
                             if li.a]

            # Get max pages
            max_pages = int(page_listings[-1][-2:])

        except Exception as e:
            max_pages = 1
            print(f"Failed to retrieve search result from source page. Status code: {str(e)}")

        return max_pages

    def job_search_driver(job_title, page_no):
        # Set up Chrome options in headless mode
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Run Chrome in headless mode
        chrome_options.add_argument("--disable-gpu")  # Disable GPU acceleration

        # HTML url encoding for search
        job_title = job_title.replace(" ", "%20")

        search_url = "https://www.usajobs.gov/Search/Results?k=" + job_title + '&p=' + str(page_no)

        # Create a Chrome webdriver instance with the specified options
        driver = webdriver.Chrome(options=chrome_options)

        try:
            # Navigate to the URL
            driver.get(search_url)

            # Wait for the page to fully load
            time.sleep(0.5)

            # Get the HTML content after dynamic loading
            html_content = driver.page_source

            # Close the browser window
            driver.quit()

            soup = BeautifulSoup(html_content, 'html.parser')

        except Exception as e:
            soup = BeautifulSoup()
            print(f"Failed to retrieve search result from source page. Status code: {str(e)}")

        return soup

    def info_extractor(soup):
        # Find all job listings
        job_listings = soup.find_all('div', class_='usajobs-search-result--core')

        # Initialize lists to store extracted information
        job_titles = []
        departments = []
        companies = []
        locations = []
        salaries = []

        # Loop through each job listing
        for job_listing in job_listings:
            job_titles.append(job_listing.find('a', class_='usajobs-search-result--core__title').text.strip())
            departments.append(job_listing.find('h4', class_='usajobs-search-result--core__agency').text.strip())
            companies.append(job_listing.find('h5', class_='usajobs-search-result--core__department').text.strip())
            locations.append(job_listing.find('h4', class_='usajobs-search-result--core__location').text.strip())
            salaries.append(job_listing.find('li', class_='usajobs-search-result--core__item').text.strip())

        # Create a DataFrame
        data = {
            'job title': job_titles,
            'agency': departments,
            'department': companies,
            'location': locations,
            'salary': salaries
        }

        df = pd.DataFrame(data)
        return df

    def scrape_usajobs(job_titles, sample):
        # URL of the USAJOBS website
        url = "https://www.usajobs.gov/"

        # output_df = pd.DataFrame()

        # Send a GET request to the URL
        response = requests.get(url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the HTML content of the page using BeautifulSoup
            soup = BeautifulSoup(response.text, 'html.parser')

            for title in job_titles:
                print("\n" + title + " started")
                max_pages = page_search_driver(title)

                if sample == "Sample":
                    max_pages = 4
                else:
                    max_pages = max_pages + 1

                for i in range(1, max_pages):
                    soup = job_search_driver(title, i)
                    df = info_extractor(soup)
                    df['search_keyword'] = title
                    df.to_csv("Final_Data/" + sample + "/USA_JOBS_" + title + "_" + str(i) + ".csv", index=False)
                    print(str(i) + " page done")
        else:
            print(f"Failed to retrieve source page. Status code: {response.status_code}")

    # Find job listings based on specific job titles
    job_titles = [
        "Data Analyst",
        "Data Engineer",
        "Business Analyst",
        "Product Manager",
        "Project Manager",
        "Mechanical Engineer",
        "Civil Engineer",
        "Software Engineer"
    ]

    print('\n Currently Fetching the Jobs from USA-JOBS')
    scrape_usajobs(job_titles, sample)
