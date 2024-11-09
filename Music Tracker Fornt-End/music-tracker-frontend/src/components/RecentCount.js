import { useState, useEffect } from "react";

const RecentCount = () => {
    const [data, setData] = useState(0);

    useEffect(() => {
        fetch(`http://127.0.0.1:5000/recent-count`)
          .then((response) => response.json())
          .then((jsonData) => setData(jsonData))
          .catch((error) => console.log(error));
      }, []);
      console.log(data);
    return (
        <>
            <p>
                {data}
            </p>

        </>
    )
}

export default RecentCount;