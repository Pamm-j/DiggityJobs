import React, { useState } from "react";
import { useJobs } from "../JobsProvider";

function AddJobForm() {
  const [formData, setFormData] = useState({
    company: "",
    job_title: "",
    link: "",
    source: "",
    applied: false,
    status: "open",
    outreach: {
      peer: 0,
      manager: 0,
      recruiter: 0,
    },
  });

  const { createJob } = useJobs();

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData((prevFormData) => ({
      ...prevFormData,
      [name]: type === "checkbox" ? checked : value,
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log(formData);
    createJob(formData);
  };

  return (
    <div>
      <div className="text-xl font-bold rounded mt-4"> Add Job Manually</div>
      <form onSubmit={handleSubmit} className="bg-almondWhite p-4 rounded">
        <div className="mb-4">
          <label htmlFor="company" className="block text-almondBrown">
            Company
          </label>
          <input
            type="text"
            id="company"
            name="company"
            value={formData.company}
            onChange={handleChange}
            className=" p-2 border border-almondSoftBlue rounded"
          />
        </div>

        <div className="mb-4">
          <label htmlFor="job_title" className="block text-almondBrown">
            Job Title
          </label>
          <input
            type="text"
            id="job_title"
            name="job_title"
            value={formData.job_title}
            onChange={handleChange}
            className=" p-2 border border-almondSoftBlue rounded"
          />
        </div>

        <div className="mb-4">
          <label htmlFor="link" className="block text-almondBrown">
            Job Link
          </label>
          <input
            type="text"
            id="link"
            name="link"
            value={formData.link}
            onChange={handleChange}
            className=" p-2 border border-almondSoftBlue rounded"
          />
        </div>

        <div className="mb-4">
          <label htmlFor="source" className="block text-almondBrown">
            Source
          </label>
          <input
            type="text"
            id="source"
            name="source"
            value={formData.source}
            onChange={handleChange}
            className=" p-2 border border-almondSoftBlue rounded"
          />
        </div>

        <div className="mb-4 flex items-center">
          <input
            type="checkbox"
            id="applied"
            name="applied"
            checked={formData.applied}
            onChange={handleChange}
            className="mr-2"
          />
          <label htmlFor="applied" className="text-almondBrown">
            Applied?
          </label>
        </div>

        <button
          type="submit"
          className="bg-almondSoftBlue text-white p-2 rounded"
        >
          Add Job
        </button>
      </form>
    </div>
  );
}

export default AddJobForm;
