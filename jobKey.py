import time
from DrissionPage import ChromiumPage
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By

expl_lvl = ['MID_LEVEL']
job_ = 'Software+Engineer'
location = 'United+States'
category_code = 'SE_Test'
start = 0

pagination_url = 'https://www.indeed.com/jobs?q={}&l={}&sc={}&start={}&from=searchOnHP&filter=0&sort=date'

p_url = ''

page = ChromiumPage()

for e in expl_lvl:
	page.get(pagination_url.format(job_, location, '0kf:explvl(' + e + ');', start))
	page.wait.load_complete()

	err = False
	while not err:
		try:
			page.wait.ele_display('.resultContent', timeout=20)
			err = True
		except Exception:
			time.sleep(10)

	soup = BeautifulSoup(page.html, 'lxml')

	t_job = soup.find_all('div', {'class': 'jobsearch-JobCountAndSortPane-jobCount'})
	total_jobs = int(t_job[0].find('span').text.split(' jobs')[0].replace(',', ''))

	jobs_list_upper = []

	st = time.time()

	limit = False

	while len(jobs_list_upper) <= total_jobs:
		l_ = 'Currently at Page ' + str((start // 10) + 1).ljust(3) + ' of job ' + category_code + ' for ' + e
		l_ = l_ + '. Fetched ' + '{:3.2f}'.format((len(jobs_list_upper) / total_jobs) * 100) + '% jobs in this category'
		l_ = l_ + '. Remaining ' + str(total_jobs - len(jobs_list_upper)).ljust(len(str(total_jobs))) + ' jobs'
		l_ = l_ + '. Completed ' + str(len(jobs_list_upper)).ljust(len(str(total_jobs))) + ' jobs.'

		print(l_)

		if len(jobs_list_upper) != 0:
			if limit:
				page.get(p_url.format(start))

			err = False
			while not err:
				try:
					page.wait.ele_display((By.XPATH, '//*[@id="mosaic-provider-jobcards"]/ul/li[1]/div'), timeout=20)
					err = True
				except Exception:
					time.sleep(10)

		soup = BeautifulSoup(page.html, 'lxml')
		jobs = soup.find_all('div', {'class': 'cardOutline'})

		jobs_list = []
		for j in jobs:
			a = {}
			try:
				a['jobKey'] = j.find('a').get('data-jk')

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
				jobs_list_upper.append(a)

				time.sleep(0.4)

			except Exception:
				pass

		with open(category_code + '_' + e + '.tsv', 'a', encoding='utf-8') as outfile:
			for i in jobs_list:
				b = '\t'.join(i.values())
				outfile.write(b + '\n')
		outfile.close()

		with open(category_code + '_' + e + '.log', 'a') as outfile:
			outfile.write(l_ + '\n')

		outfile.close()

		start = start + 10

		if not limit:
			try:
				page.ele((By.CSS_SELECTOR, 'a[data-testid=pagination-page-next]')).click()
			except Exception:
				limit = True
				fgh = page.url.split('&start=' + str(start - 10))
				p_url = fgh[0] + '&start={}' + fgh[1]

	end = time.time()
	difference = end - st

	minute = difference / 60

	with open(category_code + '_' + e + '.log', 'a') as outfile:
		outfile.write('\n\nThe time taken to run this job is ' + str(round(minute, 2)) + '\n')
	outfile.close()

	start = 0

page.quit()
