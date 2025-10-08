import React, { useState,useEffect } from "react";
import JobUpload from "./components/JobUpload";
import ResumeUpload from "./components/ResumeUpload";
import Results from "./components/Results";



const API_URL = "https://job-matcher-ai.onrender.com";
export default function App() {
  const [jobId, setJobId] = useState(null);
  const [candidateIds, setCandidateIds] = useState([]);
   useEffect(() => {
    // Ping backend once when app loads
    const wakeBackend = async () => {
      try {
        const res = await fetch(`${API_URL}/`);
        if (res.ok) {
          console.log("✅ Backend awake and ready!");
        } else {
          console.warn("⚠️ Backend ping failed:", res.status);
        }
      } catch (error) {
        console.error("❌ Backend not reachable:", error);
      }
    };
    wakeBackend();
  }, []);
  
  

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
