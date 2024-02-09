import React from "react";
import JobCard from "./JobCard";
import { useJobs } from "../JobsProvider"; // Update with the correct path

export default function JobCards() {
  const { jobs } = useJobs();

  // Group jobs by company
  const jobsByCompany = jobs.reduce((acc, job) => {
    acc[job.company] = acc[job.company] || [];
    acc[job.company].push(job);
    return acc;
  }, {});

  const numApps = jobs.filter((job) => job.applied).length;

  // Separate grouped jobs into applied and not applied
  const appliedJobs = {};
  const notAppliedJobs = {};

  Object.keys(jobsByCompany).forEach((company) => {
    const filteredAppliedJobs = jobsByCompany[company].filter(
      (job) => job.applied
    );
    const filteredNotAppliedJobs = jobsByCompany[company].filter(
      (job) => !job.applied
    );

    if (filteredAppliedJobs.length > 0) {
      appliedJobs[company] = filteredAppliedJobs;
    }

    if (filteredNotAppliedJobs.length > 0) {
      notAppliedJobs[company] = filteredNotAppliedJobs;
    }
  });

  return (
    <div className="flex flex-wrap">
      <div className="w-1/2 px-2 ">
        <h2 className="text-xl font-bold mb-3">Not Applied</h2>
        {Object.entries(notAppliedJobs).map(([company, jobs]) => (
          <div key={company}>
            <div className="border border-almondGreen rounded-lg p-3 mb-3">
              <h3 className="text-lg font-semibold ">{company}</h3>
              {jobs.map((job) => (
                <JobCard key={job.link} job={job} />
              ))}
            </div>
          </div>
        ))}
      </div>
      <div className="w-1/2 px-2">
        <h2 className="text-xl font-bold mb-3">{`Applied: ${numApps}`}</h2>
        {Object.entries(appliedJobs).map(([company, jobs]) => (
          <div key={company}>
            <div className="border border-almondGreen rounded-lg pl-2 py-2 mb-3">
              <h3 className="text-lg font-semibold">{company}</h3>
              {jobs.map((job) => (
                <JobCard key={job.link} job={job} />
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
