from fastapi import FastAPI, Depends
from pymongo import MongoClient
from pymongo.collection import Collection
from pydantic import BaseModel, Field
from typing import List, Union, Optional
from datetime import datetime
import os

from fastapi.middleware.cors import CORSMiddleware
from built import scrape_built_pages
from fastapi import HTTPException, BackgroundTasks
from bson import ObjectId


### Pydantic models ###
class OutReachCounts(BaseModel):
    """
    Represents outreach counts for a job listing, tracking interactions with peers, managers, and recruiters.
    """
    peer: int = Field(default=0, description="Number of peer interactions")
    manager: int = Field(default=0, description="Number of manager interactions")
    recruiter: int = Field(default=0, description="Number of recruiter interactions")

class OutreachUpdate(BaseModel):
    """
    Defines the structure for updating outreach counts, specifying the job link, outreach type, and action to perform.
    """
    job_link: str = Field(..., description="The unique link of the job")
    outreach_type: str = Field(..., description="The type of outreach ('peer', 'manager', 'recruiter')")
    action: str = Field(..., description="The action to perform ('increment' or 'decrement')")

class JobListing(BaseModel):
    """
    Represents a job listing, including company, job title, link, source, application status, and outreach interactions.
    """
    company: str = Field(..., description="Name of the company offering the job")
    job_title: str = Field(..., description="Title of the job")
    link: str = Field(..., description="Unique link to the job listing")
    source: str = Field(..., description="Source of the job listing, e.g., 'Built.in'")
    applied: Union[bool, datetime] = Field(False, description="Indicates if the job has been applied to, and when")
    status: Optional[str] = Field(None, description="Current status of the job application ('applied', 'deleted', 'rejected')")
    outreach: Optional[OutReachCounts] = Field(default_factory=OutReachCounts, description="Counts of outreach interactions")


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://test"],
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

def get_db():
    client = MongoClient("mongodb://localhost:27017/")
    db_name = "test_job_database" if os.getenv('TESTING') == 'True' else "job_database"
    db = client[db_name]
    return db.jobs

def get_job_by_link(jobs_collection: Collection, job_link: str):
    """
    Fetches a job from the database using its unique link.

    Parameters:
    - jobs_collection (Collection): The MongoDB collection containing job listings.
    - job_link (str): The unique link of the job to be fetched.

    Returns:
    - dict: The job document if found.

    Raises:
    - HTTPException: If no job is found with the given link, raises a 404 error.
    """
    job = jobs_collection.find_one({"link": job_link})
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job

@app.get("/jobs", response_model=List[JobListing])
async def read_jobs(jobs_collection=Depends(get_db)):
    """
    Retrieves a list of all job listings that have not been marked as 'deleted' from the database.

    Parameters:
    - jobs_collection (Depends): Dependency injection to provide the MongoDB collection for jobs.

    Returns:
    - List[JobListing]: A list of job listings as per the JobListing model.
    """
    jobs = list(jobs_collection.find(
        {"$or": [{"status": {"$ne": "deleted"}}, {"status": {"$exists": False}}]},
        {"_id": 0, "company": 1, "job_title": 1, "link": 1, "source": 1, "applied": 1, "status": 1, "outreach": 1}
    ))

    return jobs

@app.get("/job", response_model=JobListing)
async def read_job(job_link: str, jobs_collection=Depends(get_db)):
    """
    Fetches a single job listing using its unique link.

    Parameters:
    - job_link (str): The unique link of the job to be fetched.
    - jobs_collection (Depends): Dependency injection to provide the MongoDB collection for jobs.

    Returns:
    - JobListing: The job listing matching the provided link as per the JobListing model.
    """
    job = get_job_by_link(jobs_collection, job_link)
    return job

from fastapi import HTTPException

@app.post("/job", response_model=JobListing, status_code=201)
async def create_job(job_data: JobListing, jobs_collection=Depends(get_db)):
    """
    Adds a new job listing to the database.

    Parameters:
    - job_data (JobListing): The job data to be added, provided as a JSON body of the request.
    - jobs_collection (Depends): Dependency injection to provide the MongoDB collection for jobs.

    Returns:
    - JobListing: The newly added job listing as per the JobListing model.

    Raises:
    - HTTPException: An HTTP 400 error if the job with the given link already exists.
    """
    print(job_data)
    existing_job = jobs_collection.find_one({"link": job_data.link})
    if existing_job:
        raise HTTPException(status_code=400, detail="Job with the given link already exists")

    # MongoDB will automatically generate an _id for the new job
    jobs_collection.insert_one(job_data.model_dump())

    # Return the newly created job data, excluding the MongoDB generated _id
    return {k: v for k, v in job_data.model_dump().items() if k != "_id"}



@app.put("/jobs/update/status")
async def update_status(job_link: str, action: str, jobs_collection=Depends(get_db)):
    """
    Updates the status of a job identified by its link. If the action is 'applied',
    it also sets the current timestamp to the 'applied' field of the job. If the job
    doesn't exist or no document is matched for the given job link, it raises an HTTP
    404 error.

    Parameters:
    - job_link (str): The unique link of the job to be updated.
    - action (str): The new status to set for the job. If the action is 'applied',
        it also updates the 'applied' timestamp.
    - jobs_collection: The MongoDB collection instance, injected via FastAPI's 
        Dependency Injection system.

    Returns:
    - dict: A message indicating the successful update of the job status.

    Raises:
    - HTTPException: An HTTP 404 error if no job is found with the given link.
    """
    update_fields = {"status": action}
    
    if action == "applied":
        update_fields["applied"] = datetime.now()

    result = jobs_collection.update_one({"link": job_link}, {"$set": update_fields})

    # Check if any document was actually updated
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Job not found")

    return {"msg": f"Job marked {action}"}

@app.put("/outreach/update_outreach")
async def update_outreach(update: OutreachUpdate, jobs_collection=Depends(get_db)):
    """
    Updates the outreach counters for a specific job identified by its link based on the
    specified outreach type (peer, manager, or recruiter) and action (increment or decrement).
    If the job does not exist, it raises an HTTP 404 error. If the action is invalid, it raises
    an HTTP 400 error.

    Parameters:
    - update (OutreachUpdate): An instance of the OutreachUpdate Pydantic model, containing
      the job link, the type of outreach to be updated, and the action (increment or decrement).
    - jobs_collection: The MongoDB collection instance, injected via FastAPI's Dependency
      Injection system.

    Returns:
    - dict: A message indicating that the outreach counters were successfully updated.

    Raises:
    - HTTPException: An HTTP 404 error if no job is found with the given link or an HTTP 400 error
      if an invalid action is specified.
    """
    # get the job to be sure it exists before updating it
    get_job_by_link(jobs_collection, update.job_link)

    # Determine the field to update based on the outreach type
    field_to_update = f"outreach.{update.outreach_type}"

    # Update logic based on action
    if update.action == "increment":
        new_value = { "$inc": { field_to_update: 1 } }
    elif update.action == "decrement":
        new_value = { "$inc": { field_to_update: -1 } }
    else:
        raise HTTPException(status_code=400, detail="Invalid action")

    # Update the document
    jobs_collection.update_one({"link": update.job_link}, new_value)
    return {"message": "Outreach updated successfully"}


@app.put("/scrape/built")
async def scrape_built(background_tasks: BackgroundTasks, days: int = None):  # Set default to None
    """
    Your existing docstring...
    """
    # Check if days parameter is provided and is a positive integer
    if days is None or days <= 0:
        raise HTTPException(status_code=400, detail="Invalid number of days provided. Please provide a positive integer.")

    background_tasks.add_task(scrape_built_pages, days)
    return {"msg": "Scraping started"}