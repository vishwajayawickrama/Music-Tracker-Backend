import { useState, useEffect } from "react";
import './RecentTrack.css';

const RecentTracks = () => {
    const [data, setData] = useState([]);

    const fetchTracks = () => {
        fetch(`http://127.0.0.1:5000/recent-tracks`)
          .then((response) => response.json())
          .then((jsonData) => setData(jsonData))
          .catch((error) => console.log(error));
    }

    useEffect(() => {
        fetchTracks();

        const interval = setInterval(fetchTracks, 20000);

        return () => clearInterval(interval);
      }, []);
      console.log(data);
    return (
        <>
        <div className="bg-gray-100 rounded-lg p-3 w-full max-w-md ml-5 shadow-md">
            <h2 className="text-lg font-bold mb-3 text-gray-700">Recent Tracks</h2>
            <div className="space-y-2">
            {data.slice(0, 3).map((track) => (
                <div key={track.track_name} className="bg-blue-800 rounded-md p-4 flex justify-between items-center">
                    <div>
                        <p className="text-white font-semibold">{track.track_name}</p>
                        <p className="text-blue-300 text-sm">{track.artist_name}</p>
                    </div>
                </div>
            ))}
            </div>
        </div>
</>

    )
}

export default RecentTracks;