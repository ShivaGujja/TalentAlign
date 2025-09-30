import React, { useState } from "react";

const API_URL = "http://127.0.0.1:8000";

export default function Results({ jobId, candidateIds }) {
  const [results, setResults] = useState([]);

  const handleAnalyze = async () => {
    const res = await fetch(`${API_URL}/analyze`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ job_id: jobId, candidate_ids: candidateIds }),
    });
    const data = await res.json();
    setResults(data.results);
  };

  return (
    <div className="p-4 border rounded-lg bg-gray-50">
      <h2 className="text-lg font-semibold mb-2">Analysis Results</h2>
      <button
        onClick={handleAnalyze}
        className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
      >
        Run Analysis
      </button>

      {results.length > 0 && (
        <ul className="mt-4 space-y-2">
          {results.map((r) => (
            <li
              key={r.candidate_id}
              className="p-2 border rounded bg-white shadow"
            >
              <p className="font-semibold">Candidate: {r.filename}</p>
              <p>Overall Match: {r.result.overall_match}%</p>
              <p className="text-sm text-gray-600">
                {r.result.explanation}
              </p>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
