from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests

import pandas as pd

#specify the driver path with the proper driver for Firefox, open indeed.com
###DRIVER_PATH = '/Users/claytondarlington/Projects/jobAggregator/geckodriver'
###driver = webdriver.Firefox(executable_path=DRIVER_PATH)
driver = webdriver.Safari()
driver.get('https://ca.indeed.com/')

#search for software developer with auto fill in the location
searchJob = driver.find_element_by_xpath('//input[@id="text-input-what"]')
searchJob.send_keys(['software developer'])

#search button interaction
searchButton = driver.find_element_by_xpath('//*[@id="whatWhereFormId"]/div[3]/button')
searchButton.click()



driver.implicitly_wait(3)

#extract the relevant info that I want
titles = []
companies = []
locations = []
links = []
reviews = []
salaries = []
descriptinos = []

for i in range(0,1):

##close a possible email signup pop-up
    try:
        closePop = driver.find_element_by_xpath('.//button[@class="popover-x-button-close icl-CloseButton"]')
        closePop.click()
    except:
        print('No pop')
    
    jobPost = driver.find_elements_by_xpath('//div[contains(@class,"clickcard")]')

    for job in jobPost:

        company = job.find_element_by_xpath('.//span[@class="company"]').text
        print(company)
        try:
            location = job.find_element_by_xpath('.//span[contains(@class,"location")]').text
        except:
            location = 'None'

        try: 
            title = job.find_element_by_xpath('.//h2[@class="title"]//a').text
        except:
            title = job.find_element_by_xpath('.//h2[@class="title"]//a').get_attribute(name="title")

        try:
            salary = job.find_element_by_xpath('.//span[contains(@class, "salaryText")]').text
        except:
            salary = 'None'

        link = job.find_element_by_xpath('.//h2[@class="title"]//a').get_attribute(name="href")

        links.append(link)
        salaries.append(salary)
        titles.append(title)
        companies.append(company)
        locations.append(location)

##go to next page
    try:
        nextPage = driver.find_element_by_xpath('.//a[@aria-label={}]//span[@class="pn"]')
        nextPage.click()
    except:
        nextPage = driver.find_element_by_xpath('.//a[@aria-label="Next"]//span[@class="np"]')
        nextPage.click()

##Get the full description of the jobs 
descriptions = []

for link  in links:

    check = requests.get(link)
    print(check)

    if check.status_code == 200:
        try:
            driver.get(link)
            jobDesc = driver.find_element_by_xpath('.//div[@id="jobDescriptionText"]').text
            descriptinos.append(jobDesc)
        except:
            print("Error loading description")

    


##write to a file for now
jobsDF = pd.DataFrame()

jobsDF['Title'] = titles
jobsDF['Company'] = companies
jobsDF['Location'] = locations
jobsDF['Link'] = links
jobsDF['Salary'] = salaries
jobsDF['Description'] = descriptinos

jobsDF.to_csv("jobs.csv", index=False)
