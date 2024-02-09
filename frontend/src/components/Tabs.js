import React, { useState } from "react";
import JobListingsPage from "./JobListingsPage";
import AddJob from "./AddJob";
import Tab from "./Tab";

function Tabs() {
  const [activeTab, setActiveTab] = useState("Job Apps");

  return (
    <div className="bg-almondWhite text-almondBrown flex flex-col items-start w-full">
      <div className="tabs pt-4 pl-4 mb-4 border-b-4 border-almondSaturatedBlue w-full flex">
        <Tab
          setActiveTab={setActiveTab}
          text={"Job Apps"}
          activeTab={activeTab}
        />
        <Tab
          setActiveTab={setActiveTab}
          text={"Add Jobs"}
          activeTab={activeTab}
        />
      </div>
      <div
        className={`tab-content bg-lighterAlmondWhite p-4${
          activeTab === "Job Apps" || activeTab === "Add Jobs"
            ? "border-t-0"
            : ""
        }`}
      >
        <div className="ml-4">
          {activeTab === "Job Apps" && <JobListingsPage />}
          {activeTab === "Add Jobs" && <AddJob />}
        </div>
      </div>
    </div>
  );
}

export default Tabs;
