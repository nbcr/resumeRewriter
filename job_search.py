import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from generate_cover_letter import has_applied_to_job

def initialize_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    service = Service("C:/Apps/chromedriver/chromedriver.exe")
    return webdriver.Chrome(service=service, options=chrome_options)

def fetch_job_postings(driver, url, max_jobs=3):
    driver.get(url)
    all_job_postings = []
    
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/main/form[2]/section/div[2]/div[1]/div[3]/article'))
        )
        jobs = driver.find_elements(By.XPATH, '/html/body/main/form[2]/section/div[2]/div[1]/div[3]/article')
        
        for job in jobs:
            try:
                title_element = job.find_element(By.XPATH, './a/h3/span[3]')
                title = title_element.text.strip()
                job_url = job.find_element(By.XPATH, './a').get_attribute('href')
                company = job.find_element(By.XPATH, './a/ul/li[2]').text.strip()
                location = job.find_element(By.XPATH, './a/ul/li[3]').text.strip()
                
                try:
                    salary = job.find_element(By.XPATH, './a/ul/li[4]').text.strip()
                except NoSuchElementException:
                    salary = 'Not specified'
                
                all_job_postings.append({
                    'title': title,
                    'company': company,
                    'location': location,
                    'salary': salary,
                    'url': job_url
                })
            
            except NoSuchElementException:
                continue

    except TimeoutException:
        print("Timeout while loading job postings.")
    
    # Filter out already-applied jobs and limit to `max_jobs`
    unique_jobs = []
    for job in all_job_postings:
        if has_applied_to_job(job):  # Passing the entire job dictionary here
            print(f"Skipping already applied job: {job['title']} at {job['company']}")
            continue
        unique_jobs.append(job)
        if len(unique_jobs) >= max_jobs:
            break

    return unique_jobs
