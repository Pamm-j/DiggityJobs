// OutreachCounter.js
import React, { useState } from "react";
import { useJobs } from "../JobsProvider";

function OutreachCounter({ type, initialCount, job }) {
  const [count, setCount] = useState(initialCount);
  const { handleOutreach } = useJobs();

  const handleIncrement = () => {
    const newCount = count + 1;
    setCount(newCount);
    handleOutreach(job.link, type, "increment");
  };

  const handleDecrement = () => {
    if (count > 0) {
      const newCount = count - 1;
      setCount(newCount);
      handleOutreach(job.link, type, "decrement");
    }
  };

  return (
    <div>
      <button className="text-almondPink" onClick={handleDecrement}>-</button>
      <span>
        {" "}
        {type}: {count}{" "}
      </span>
      <button className="text-almondPink" onClick={handleIncrement}>+</button>
    </div>
  );
}

export default OutreachCounter;
