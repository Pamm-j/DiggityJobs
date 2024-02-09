import React from "react";
import OutreachCounter from "./OutreachCounter";
import { useJobs } from "../JobsProvider";

export default function JobDetails({ job }) {
  const generateDate = (dateObj) => {
    if (dateObj === true) return "a few";
    const givenDate = new Date(dateObj);
    const currentDate = new Date();
    const differenceInTime = currentDate.getTime() - givenDate.getTime();
    const differenceInDays = Math.floor(differenceInTime / (1000 * 3600 * 24));
    return String(differenceInDays);
  };
  const { handleStatus } = useJobs();

  return (
    <div className="max-w-md mx-auto p-4 bg-white rounded-lg shadow-lg">
      <div className="mb-4">
        {job.applied && (
          <p className="text-center text-almondBlue">
            Applied {generateDate(job.applied)} days ago
          </p>
        )}

        <p className="text-center text-almondBlue">
          App Status: {job.status ? job.status : "Applied"}
        </p>
      </div>

      <div className="border-t pt-2 pb-2">
        <h3 className="text-lg font-semibold mb-2">Job Outreach</h3>
        <div className="grid grid-cols-3 gap-4 items-start">
          <OutreachCounter
            type="peer"
            initialCount={job.outreach.peer}
            job={job}
          />
          <OutreachCounter
            type="manager"
            initialCount={job.outreach.manager}
            job={job}
          />
          <OutreachCounter
            type="recruiter"
            initialCount={job.outreach.recruiter}
            job={job}
          />
        </div>
      </div>
      <div className="border-t pt-2">
        <h3 className="text-lg font-semibold mb-2">Actions</h3>
        {job.status !== "rejected" && (
          <div className="flex space-x-4">
            {!job.applied && (
              <button onClick={() => handleStatus(job, "applied")}>
                Applied
              </button>
            )}

            <button onClick={() => handleStatus(job, "deleted")}>Remove</button>
            {job.applied && (
              <button onClick={() => handleStatus(job, "rejected")}>
                Rejected
              </button>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
