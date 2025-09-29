import React, { useState } from "react";
import JobUpload from "./components/JobUpload";
// import ResumeUpload from "./components/ResumeUpload";
// import Results from "./components/Results";

function App() {
  const [jobId, setJobId] = useState(null);
  const [results, setResults] = useState([]);

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-500 via-purple-600 to-pink-500 flex items-center justify-center p-8">
      <div className="bg-white shadow-2xl rounded-2xl w-full max-w-3xl p-6 space-y-6">
        <h1 className="text-3xl font-bold text-center text-indigo-600">
          🚀 Job Matcher AI
        </h1>

        {/* Upload Job */}
        <JobUpload setJobId={setJobId} />

        {/* Upload Resume */}
        {jobId && <ResumeUpload jobId={jobId} setResults={setResults} />}

        {/* Show Results */}
        {results.length > 0 && <Results results={results} />}
      </div>
    </div>
  );
}

export default App;
