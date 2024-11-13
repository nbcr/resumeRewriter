import openai
import os
from file_utils import sanitize_filename

# Set your OpenAI API key here
openai.api_key = "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"  # Replace with your actual API key

def generate_cover_letter(job, contact_info):
    # Construct a prompt for generating a cover letter
    prompt = f"""
    Write a professional and customized cover letter for the following job:

    Job Title: {job['title']}
    Company: {job['company']}
    Location: {job['location']}
    Salary: {job['salary']}
    Job URL: {job['url']}

    Candidate Info:
    Name: {contact_info['name']}
    Email: {contact_info['email']}
    Phone: {contact_info['phone']}
    Location: {contact_info['address']}

    The cover letter should be engaging, personalized, and reflect the candidate's extensive experience in related fields.
    """

    # Generate cover letter content with OpenAI
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=500,
        temperature=0.75
    )

    cover_letter = response['choices'][0]['message']['content']
    return cover_letter

def log_applied_job(job):
    job_url = job.get('url', '').strip()
    with open('applied_jobs.txt', 'a') as file:
        file.write(job_url + '\n')

def has_applied_to_job(job):
    job_url = job.get('url', '').strip()  # Access the URL directly from the job dictionary

    try:
        with open('applied_jobs.txt', 'r') as file:
            applied_jobs = file.readlines()
        return any(job_url == line.strip() for line in applied_jobs)
    except FileNotFoundError:
        return False
