// JobListingsPage.js
import React, { useEffect } from "react";
import JobCards from "./JobCards";
import { useJobs } from "../JobsProvider";

function JobListingsPage() {
  const { setJobs } = useJobs();

  useEffect(() => {
    fetch("http://localhost:8000/jobs")
      .then((response) => response.json())
      .then((data) => {
        setJobs(data);
      })
      .catch((error) => console.error("Error fetching data: ", error));
  }, [setJobs]);

  return (
    <div>
      <JobCards />
    </div>
  );
}

export default JobListingsPage;
