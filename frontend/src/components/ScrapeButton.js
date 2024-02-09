import React, { useState } from "react";
import axios from "axios";

export default function ScrapeButton() {
  const [daysToScrape, setDaysToScrape] = useState(1);

  const scrapeBuilt = (days) => {
    axios
      .put(`http://localhost:8000/scrape/built?days=${days}`)
      .then(() => console.log("I tried my best to scrape that bitch"))
      .catch((error) => console.error("Error scraping BuiltIn:", error));
  };

  const incrementDays = () => {
    if (!daysToScrape) {
      setDaysToScrape(1);
    } else {
      setDaysToScrape(daysToScrape + 1);
    }
  };
  const decrementDays = () => {
    if (!daysToScrape) {
      setDaysToScrape(1);
    } else if (daysToScrape <= 1) {
      return;
    } else {
      setDaysToScrape(daysToScrape - 1);
    }
  };

  return (
    <>
      <div className="flex items-center mr-2 flex-row"></div>
      <div>
        {" "}
        <span className="text-xl font-bold rounded">Scrape BuiltIn</span>
        <span> for the past </span>
        <button onClick={decrementDays} className="text-xl">
          -
        </button>
        <input
          type="text"
          readOnly
          value={`${daysToScrape} day${daysToScrape > 1 ? "s" : ""}`}
          className="w-14 text-center text-almondBrown bg-almondWhite rounded mx-1"
        />
        <button onClick={incrementDays} className="text-xl">
          +
        </button>{" "}
        <button
          className="text-white p-2 ml-4 bg-almondSoftBlue rounded"
          onClick={() => scrapeBuilt(daysToScrape)}
        >
          Scrape{" "}
        </button>
      </div>
    </>
  );
}
