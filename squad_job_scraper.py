import requests
from bs4 import BeautifulSoup

# Fetch the webpage content
url = "https://squadjobs.com/jobs?text=software+engineer"
response = requests.get(url)
html_content = response.text

# Parse the HTML content
soup = BeautifulSoup(html_content, 'html.parser')
print(soup)

# Find all job listings
jobs = soup.find_all('tr', class_="even:bg-zinc-50")

# Filter for 'Entry-level' jobs
entry_level_jobs = [job for job in jobs if job.find('span', text="Entry-level")]

# Extract and print job titles and links for 'Entry-level' jobs
for job in entry_level_jobs:
    title = job.find('h3', {'data-test-id': 'job-title'}).text
    link = job.find('a')['href']
    print(f"Job Title: {title}, Link: {link}")
