import React, { useEffect } from "react";
// import JobCards from "./components/JobCards";
import { useJobs } from "./JobsProvider";
// import ScrapeButton from "./components/ScrapeButton";
import Tabs from "./components/Tabs";

function App() {
  const { setJobs } = useJobs();


  useEffect(() => {
    fetch("http://localhost:8000/jobs")
      .then((response) => response.json())
      .then((data) => {
        setJobs(data);
        console.log(data);
      })
      .catch((error) => console.error("Error fetching data: ", error));
  }, []);


  return (
    <div className="bg-almondWhite text-almondBrown flex flex-col items-start">
      <Tabs/>
    </div>
  );
}

export default App;
