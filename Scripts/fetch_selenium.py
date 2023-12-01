import time

import requests
import undetected_chromedriver as uc
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium_stealth import stealth

ua = UserAgent(min_percentage=1.7)

option = webdriver.ChromeOptions()

# Going undercover:
option.headless = False
option.user_agent = ua.random
# option.add_argument('--incognito')

expl_lvl = ['SENIOR_LEVEL', 'MID_LEVEL']
job_ = 'Business+Analyst'
location = 'United+States'
category_code = 'BA'
start = 0

pagination_url = 'https://www.indeed.com/jobs?q={}&l={}&sc={}&start={}&from=searchOnHP'

driver = uc.Chrome(options=option, driver_executable_path='/Users/pragyanaryal/Downloads/undetected_chromedriver')

stealth(
    driver,
    languages=['en-US', 'en'],
    vendor='Google Inc.',
    platform='Win64',
    webgl_vendor='Intel Inc.',
    renderer='Intel Iris OpenGL Engine',
    fix_hairline=True,
)


def internet_connection():
    try:
        requests.get('https://google.com', timeout=5)
        return True
    except requests.ConnectionError:
        return False


for e in expl_lvl:
    try:
        driver.get(pagination_url.format(job_, location, '0kf:explvl(' + e + ');', start))
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="mosaic-provider-jobcards"]/ul/li[1]/div')))
    except Exception:
        conn = internet_connection()

        while not conn:
            conn = internet_connection()

        driver.get(pagination_url.format(job_, location, '0kf:explvl(' + e + ');', start))
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="mosaic-provider-jobcards"]/ul/li[1]/div')))

    soup = BeautifulSoup(driver.page_source, 'lxml')
    t_job = soup.find_all('div', {'class': 'jobsearch-JobCountAndSortPane-jobCount'})
    total_jobs = int(t_job[0].find('span').text.split(' jobs')[0].replace(',', ''))

    jobs_list_upper = []

    st = time.time()

    while len(jobs_list_upper) <= total_jobs:
        l_ = 'Currently at Page ' + str((start // 10) + 1).ljust(3) + ' of job ' + category_code + ' for ' + e
        l_ = l_ + '. Fetched ' + '{:3.2f}'.format((len(jobs_list_upper) / total_jobs) * 100) + '% jobs in this category'
        l_ = l_ + '. Remaining ' + str(total_jobs - len(jobs_list_upper)).ljust(len(str(total_jobs))) + ' jobs'
        l_ = l_ + '. Completed ' + str(len(jobs_list_upper)).ljust(len(str(total_jobs))) + ' jobs.'

        print(l_)

        try:
            driver.get(pagination_url.format(job_, location, '0kf:explvl(' + e + ');', start))
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="mosaic-provider-jobcards"]/ul/li[1]/div')))
        except Exception:
            conn = internet_connection()

            while not conn:
                conn = internet_connection()

            driver.get(pagination_url.format(job_, location, '0kf:explvl(' + e + ');', start))
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="mosaic-provider-jobcards"]/ul/li[1]/div')))

        soup = BeautifulSoup(driver.page_source, 'lxml')
        jobs = soup.find_all('div', {'class': 'cardOutline'})

        jobs_list = []
        if len(jobs) > 0:
            for j in jobs:
                a = {}

                try:
                    a['company'] = j.find('span', attrs={'data-testid': 'company-name'}).text
                except Exception:
                    a['company'] = 'NA'

                try:
                    a['title'] = j.find('h2', {'class': 'jobTitle'}).text
                except Exception:
                    a['title'] = 'NA'

                try:
                    a['location'] = j.find('div', attrs={'data-testid': 'text-location'}).text
                except Exception:
                    a['location'] = 'NA'

                a['category_code'] = category_code
                a['experience_level'] = e

                try:
                    salary = j.find('div', {'class': 'metadata salary-snippet-container'}).text
                    a['salary'] = salary
                except Exception:
                    try:
                        salary = j.find('div', {'class': 'metadata estimated-salary-container'}).text
                        a['salary'] = salary
                    except Exception:
                        a['salary'] = 'NA'

                jobs_list.append(a)

            for i, _ in enumerate(jobs_list):
                try:
                    try:
                        driver.find_elements(By.CLASS_NAME, 'cardOutline')[i].click()
                        WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located((By.XPATH, '//*[@id="mosaic-provider-jobcards"]/ul/li[1]/div'))
                        )
                        time.sleep(1)
                    except Exception:
                        conn = internet_connection()

                        while not conn:
                            conn = internet_connection()

                        driver.find_elements(By.CLASS_NAME, 'cardOutline')[i].click()
                        WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located((By.XPATH, '//*[@id="mosaic-provider-jobcards"]/ul/li[1]/div'))
                        )
                        time.sleep(1)

                    y = BeautifulSoup(driver.page_source, 'lxml')
                    d = y.find_all('div', {'id': 'jobDescriptionText'})
                    g = d[0].extract()
                    f = [h.text.replace('\n', '') for h in g if h.text != '\n']

                    # This is the string of Job Description
                    a = ''.join(f)
                    jobs_list[i]['skills'] = a
                    jobs_list_upper.append(jobs_list[i])
                    time.sleep(1)
                except Exception:
                    jobs_list[i]['skills'] = 'NA'

            with open(category_code + '_' + e + '.tsv', 'a', encoding='utf-8') as outfile:
                for i in jobs_list:
                    b = '\t'.join(i.values())
                    outfile.write(b + '\n')
            outfile.close()

            with open(category_code + '_' + e + '.log', 'a') as outfile:
                outfile.write(l_ + '\n')

            outfile.close()

            time.sleep(2)
            start = start + 10

    end = time.time()
    difference = end - st

    minute = difference / 60

    with open(category_code + '_' + e + '.log', 'a') as outfile:
        outfile.write('\n\nThe time taken to run this job is ' + str(round(minute, 2)) + '\n')
    outfile.close()

    start = 0

driver.quit()
