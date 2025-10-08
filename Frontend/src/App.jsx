import React, { useState } from "react";
import JobUpload from "./components/JobUpload";
import ResumeUpload from "./components/ResumeUpload";
import Results from "./components/Results";

export default function App() {
  const [jobId, setJobId] = useState(null);
  const [candidateIds, setCandidateIds] = useState([]);

  return (
    <div className="max-w-3xl mx-auto p-6 space-y-6">
      <h1 className="text-2xl font-bold text-center text-indigo-700">
        Job Matcher AI
      </h1>

      <JobUpload setJobId={setJobId} />

      {jobId && (
        <ResumeUpload setCandidateIds={setCandidateIds} />
      )}

      {jobId && candidateIds.length > 0 && (
        <Results jobId={jobId} candidateIds={candidateIds} />
      )}
    </div>
  );
}