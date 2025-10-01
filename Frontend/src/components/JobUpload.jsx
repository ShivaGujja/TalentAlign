import React, { useState } from "react";

const API_URL = "https://job-matcher-ai.onrender.com";

export default function JobUpload({ setJobId }) {
  const [jobText, setJobText] = useState("");

  const handleUpload = async () => {
    const formData = new FormData();
    if (jobText.trim()) {
      formData.append("job_text", jobText);
    }
    const res = await fetch(`${API_URL}/upload_job`, {
      method: "POST",
      body: formData,
    });
    const data = await res.json();
    setJobId(data.job_id);
    alert("✅ Job uploaded successfully!");
  };

  return (
    <div className="p-4 border rounded-lg bg-gray-50">
      <h2 className="text-lg font-semibold mb-2">Upload Job Description</h2>
      <textarea
        className="w-full border rounded p-2 mb-2"
        rows={4}
        placeholder="Paste job description here..."
        value={jobText}
        onChange={(e) => setJobText(e.target.value)}
      />
      <button
        onClick={handleUpload}
        className="bg-indigo-600 text-white px-4 py-2 rounded hover:bg-indigo-700"
      >
        Upload Job
      </button>
    </div>
  );
}
