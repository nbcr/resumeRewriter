import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

from job_search import fetch_job_postings
from extract_resume_info import extract_info_from_resume
from generate_cover_letter import generate_cover_letter, log_applied_job, has_applied_to_job
from save_pdf import save_cover_letter_as_pdf
from file_utils import sanitize_filename

# Initialize Web Driver
def initialize_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    service = Service("C:/Apps/chromedriver/chromedriver.exe")
    return webdriver.Chrome(service=service, options=chrome_options)

# Contact information extracted from the resume
resume_file_path = "Master Resume.docx"
contact_info = extract_info_from_resume(resume_file_path)

# URL to job search page
job_search_url = "https://www.jobbank.gc.ca/jobsearch/jobsearch?page=1&sort=M&fsrc=16&mid=22408"

# Directory to save output files
output_dir = "output"
os.makedirs(output_dir, exist_ok=True)

# Set maximum number of jobs to process
max_jobs = 3

# Initialize web driver and fetch job postings
driver = initialize_driver()
job_postings = fetch_job_postings(driver, job_search_url, max_jobs=max_jobs)
driver.quit()

# Process each job posting
for job in job_postings:
    print(f"Checking job: {job['title']} at {job['company']} - URL: {job['url']}")
    
    # Check if the job has already been applied to
    if has_applied_to_job(job):
        print(f"Skipping already applied job: {job['title']} at {job['company']}")
        continue
    
    # Generate a cover letter for the job
    cover_letter_content = generate_cover_letter(job, contact_info)
    
    # Find additional company details if available
    company_details = {
        "address": "Company Address",  # Add a dynamic lookup here if necessary
        "phone": "Company Phone"
    }
    
    # Save the cover letter as a PDF
    pdf_path = save_cover_letter_as_pdf(cover_letter_content, job, contact_info, company_details)
    print(f"Cover letter saved to {pdf_path}")
    
    # Log that we've applied to this job
    log_applied_job(job)
    
    # Small delay between processing jobs
    time.sleep(2)

print("Job application process completed.")
