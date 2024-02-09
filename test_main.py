import pytest
import os
from fastapi.testclient import TestClient
from main import app 
from pymongo import MongoClient
import datetime


test_job = {
    "company": "Test Company",
    "job_title": "Test Job Title",
    "link": "http://test.com/test_job",
    "source": "Test Source",
    "applied": False,
    "status": None,
    "outreach": {"peer": 2, "manager": 1, "recruiter": 0}
}
@pytest.fixture(scope="function")
def test_client():
    # Setup
    os.environ['TESTING'] = 'True'

    client = TestClient(app)
    # Connect to the test database
    test_db_client = MongoClient("mongodb://localhost:27017/")
    test_db = test_db_client["test_job_database"]
    test_db.jobs.insert_one(test_job)

    yield client  # This client will be used for tests

    # Clean up: delete the test job and clear the TESTING environment variable
    test_db.jobs.delete_many({})
    del os.environ['TESTING']

# Test to ensure the /jobs endpoint returns a 200 status code and includes the test job
def test_read_jobs(test_client):
    response = test_client.get("/jobs")
    assert response.status_code == 200
    jobs = response.json()
    
    # Assert non-empty response and structure of the first job
    assert jobs, "Response should not be empty"
    for job in jobs:
        assert set(job.keys()) == set(test_job.keys()) - {'_id'}, "Job structure does not match expected format"
    
    # Assert presence of the test job in the response
    assert any(job for job in jobs if job['link'] == "http://test.com/test_job"), "Test job not found in response"


def test_increment_outreach(test_client):
    # Define the request data
    update_data = {"job_link": test_job["link"], "outreach_type": "peer", "action": "increment"}

    # Send the request to update outreach
    response = test_client.put("/outreach/update_outreach", json=update_data)

    # Check the response and the updated outreach counter
    assert response.status_code == 200
    updated_job = test_client.get("/job", params={"job_link": test_job["link"]}).json()
    assert updated_job["outreach"]["peer"] == 3

# Test the decrement action for the outreach
def test_decrement_outreach(test_client):
    update_data = {"job_link": test_job["link"], "outreach_type": "manager", "action": "decrement"}
    response = test_client.put("/outreach/update_outreach", json=update_data)
    assert response.status_code == 200
    updated_job = test_client.get("/job", params={"job_link": test_job["link"]}).json()
    assert updated_job["outreach"]["manager"] == 0

# Test updating outreach for a non-existing job
def test_outreach_nonexistent_job(test_client):
    update_data = {"job_link": "http://test.com/nonexistent_job", "outreach_type": "peer", "action": "increment"}
    response = test_client.put("/outreach/update_outreach", json=update_data)
    assert response.status_code == 404

# Test updating outreach with an invalid action
def test_outreach_invalid_action(test_client):
    update_data = {"job_link": test_job["link"], "outreach_type": "peer", "action": "invalid_action"}
    response = test_client.put("/outreach/update_outreach", json=update_data)
    assert response.status_code == 400

def test_update_status_success(test_client):
    # Test updating the status of an existing job
    job_link = "http://test.com/test_job"
    action = "rejected"
    response = test_client.put(f"/jobs/update/status?job_link={job_link}&action={action}")
    assert response.status_code == 200, "Expected status code to be 200 OK"
    assert response.json() == {"msg": f"Job marked {action}"}, "Expected success message not returned"

    # Verify the job status is updated in the database
    updated_job = test_client.get(f"/job?job_link={job_link}").json()
    assert updated_job['status'] == action, "Job status not updated"

def test_update_status_non_existent_job(test_client):
    # Test updating the status of a non-existent job
    job_link = "http://test.com/non_existent_job"
    action = "rejected"
    response = test_client.put(f"/jobs/update/status?job_link={job_link}&action={action}")
    assert response.status_code == 404, "Expected status code to be 404 Not Found"

def test_update_status_applied(test_client):
    # Test setting a job's status to 'applied' and updating the 'applied' timestamp
    job_link = "http://test.com/test_job"
    action = "applied"
    response = test_client.put(f"/jobs/update/status?job_link={job_link}&action={action}")
    assert response.status_code == 200, "Expected status code to be 200 OK"

    # Verify the job's 'applied' field is updated in the database
    updated_job = test_client.get(f"/job?job_link={job_link}").json()
    assert updated_job['status'] == action, "Job status not updated to 'applied'"
    assert 'applied' in updated_job, "Job 'applied' timestamp not set"
    # Optionally, verify the 'applied' timestamp is recent, considering possible delays in test execution

def test_scrape_built_no_days_given(test_client):
    # Call the /scrape/built endpoint without providing the 'days' parameter
    response = test_client.put("/scrape/built")
    assert response.status_code == 400

    response = test_client.put("/scrape/built?days=a")
    assert response.status_code == 422

    response = test_client.put("/scrape/built?days=0")
    assert response.status_code == 400

    # Assert that the response contains an error message about the missing 'days' parameter
    assert response.json() == {"detail": "Invalid number of days provided. Please provide a positive integer."}

# TODO:write stubbed tests for scraper
