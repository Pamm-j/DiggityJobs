import React, { createContext, useContext, useState } from "react";
import axios from "axios";

const JobsContext = createContext();

export const useJobs = () => useContext(JobsContext);

export const JobsProvider = ({ children }) => {
  const [jobs, setJobs] = useState([]);

  const handleOutreach = (updatedJobLink, type, action) => {
    axios
      .put(`http://localhost:8000/outreach/update_outreach`, {
        job_link: updatedJobLink,
        outreach_type: type,
        action: action,
      })
      .catch((error) =>
        console.error("Error updating outreach counts:", error)
      );
  };
  const createJob = (job) => {
    axios
      .post(`http://localhost:8000/job`, job)
      .catch((error) => console.error("Error adding job to db:", error));
  };

  const handleStatus = (rejectedJob, action) => {
    axios
      .put(
        `http://localhost:8000/jobs/update/status?job_link=${rejectedJob.link}&action=${action}`
      )
      .then((response) => {
        if (response.status === 200) {
          // Set the status to 'rejected' for the job and update the state
          setJobs(
            jobs.map((job) =>
              job.link === rejectedJob.link ? { ...job, status: action } : job
            )
          );
        }
      })
      .catch((error) => console.error("Error updating job status:", error));
  };

  return (
    <JobsContext.Provider
      value={{
        jobs,
        setJobs,
        handleOutreach,
        handleStatus,
        createJob,
      }}
    >
      {children}
    </JobsContext.Provider>
  );
};
