import React from "react";

export default function Tab({ activeTab, setActiveTab, text}) {
  return (
    <>
      <button
        className={`tab mr-2 py-2 px-4 inline-block ${
          activeTab === text
            ? "bg-almondSaturatedBlue text-white rounded-t-lg"
            : "bg-almondWhite hover:text-almondSaturatedBlue"
        }`}
        onClick={() => setActiveTab(text)}
      >
        {text}
      </button>
    </>
  );
}
