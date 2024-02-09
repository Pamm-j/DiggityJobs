import requests
from bs4 import BeautifulSoup
import time
import random
import pymongo

# Establish connection to MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["job_database"]  # Create a database named 'job_database'
collection = db["jobs"]  # Create a collection named 'jobs'

class JobListing:
    def __init__(self, company, job_title, link, source="builtin"):
        self.company = company
        self.job_title = job_title
        self.link = link
        self.source = source
        self.applied = False
        self.status = "fetched"

    def __str__(self):
        return f"Job Title: {self.job_title} @ {self.company} LINK: {self.link} SOURCE: {self.source} APPLIED: {self.applied}"

    def to_dict(self):
        return {
            "company": self.company,
            "job_title": self.job_title,
            "link": self.link,
            "source": self.source,
            "applied": self.applied
        }


jobs = []


def generate_built_urls(days):
    return [f"https://builtin.com/jobs/san-francisco/dev-engineering?search=software+engineer&daysSinceUpdated={days}",
             f"https://builtin.com/jobs/san-francisco/dev-engineering?search=junior&daysSinceUpdated={days}", 
             f"https://builtin.com/jobs/remote?search=software+engineer&daysSinceUpdated={days}"]

def scrape_built_page(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        job_listings = soup.find_all('div', id=lambda x: x and x.startswith('job-card'))

        for job in job_listings:
            company_name_div = job.find('div', {'data-id': 'company-title'})
            company_name = company_name_div.string

            experience = job.find('span', string="1-3 Years of Experience")
            if not experience:
                experience = job.find('span', string="1-Years of Experience")
            if experience:
                job_title_link = job.find('a', id='job-card-alias')
                if job_title_link:
                    job_title = job_title_link.string
                    excluded_keywords = ['senior', 'manager', 'staff', 'architect']
                    if not any(keyword in job_title.lower() for keyword in excluded_keywords):
                        company_name_div = job.find('div', {'data-id': 'company-title'})
                        if company_name_div:
                            company_name = company_name_div.text.strip()
                            job_link = job.find('a', id='job-card-alias')['href']
                            full_job_link = "https://builtin.com" + job_link
                            if job_link:
                                job = JobListing(job_title=job_title, company=company_name, link=full_job_link)
                                jobs.append(job)

# Scrape the first page to find out how many pages there are
def scrape_built_pages(days):
    for base_url in generate_built_urls(days):
        page_url = base_url + "&page={}"
        response = requests.get(base_url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            pagination = soup.find('ul', class_='pagination')
            pages = pagination.find_all('a') if pagination else []
            max_page = max([int(page.get_text()) for page in pages if page.get_text().isdigit()], default=1)
            print(f"there are {max_page} pages")
            # Iterate over all pages and scrape each
            for page_number in range(1, max_page + 1):
                url = base_url if page_number == 1 else page_url.format(page_number)
                scrape_built_page(url)
                time.sleep(random.uniform(1, 6))  # Random delay between 1 to 5 seconds

        count = 0
        for job in jobs:
            job_dict = job.to_dict()

            # Check if the job already exists in the database
            if collection.count_documents({'link': job_dict['link']}) == 0:
                count += 1
                collection.insert_one(job_dict)

        print(f"{count} of {len(jobs)} jobs were acceptable")
