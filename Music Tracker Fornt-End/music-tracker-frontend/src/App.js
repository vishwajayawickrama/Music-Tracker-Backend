import './App.css';
import RecentTracks from './components/RecentTrack';
import RecentCount from './components/RecentCount';

function App() {
  return (
    <div>
      <h1 className="text-3xl font-bold p-10">
        Good Evening Vishwa Jayawickrama !!
      </h1>
      <RecentTracks />
      <RecentCount />
    </div>
  );
}

export default App;
