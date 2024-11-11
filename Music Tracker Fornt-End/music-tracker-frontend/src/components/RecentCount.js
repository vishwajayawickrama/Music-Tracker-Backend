import { useState, useEffect } from "react";
import CountBox from './CountBox'

const RecentCount = () => {
    const [ today, setToday] = useState(0);
    const [ month, setMonth] = useState(0);
    const [ year, setYear] = useState(0);

    
    useEffect(() => {
      // Fetching Todays Count
        fetch(`http://127.0.0.1:5000/today-count`)
          .then((response) => response.json())
          .then((jsonData) => setToday(jsonData))
          .catch((error) => console.log(error));
        
      // Fetching Month Count
        fetch(`http://127.0.0.1:5000/month-count`)
          .then((response) => response.json())
          .then((jsonData) => setMonth(jsonData))
          .catch((error) => console.log(error));
      // Fetching Year Count
        fetch(`http://127.0.0.1:5000/year-count`)
          .then((response) => response.json())
          .then((jsonData) => setYear(jsonData))
          .catch((error) => console.log(error));
        
      }, []);
      console.log(today);
      console.log(month);
      console.log(year);
    return (
        <div className="bg-gray-100 rounded-lg w-1/3 p-1 m-4 place-items-center">
            <CountBox type="Todays Count" count={today} />
            <CountBox type="Months Count" count={month} />
            <CountBox type="Years Count" count={year} />
            

        </div>
    )
}

export default RecentCount;