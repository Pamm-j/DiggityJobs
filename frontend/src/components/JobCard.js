import React, { useState } from "react";
import JobDetails from "./JobDetails";

export default function JobCard({ job }) {
  const [showDetails, setShowDetails] = useState(false);
  return (
    <div>
      <ul className="list-disc pl-5">
        <li>
          <a
            href={job.link}
            target="_blank"
            rel="noopener noreferrer"
            className={`hover:underline font-semibold ${
              job.status === "rejected" ? "line-through" : " "
            }`}
          >
            {job.job_title}
          </a>

          <button
            className="text-almondPink pl-2"
            onClick={() => setShowDetails(!showDetails)}
          >
            {showDetails ? "Hide Details" : "Details"}
          </button>

          {showDetails && <JobDetails job={job} />}
        </li>
      </ul>
    </div>
  );
}
