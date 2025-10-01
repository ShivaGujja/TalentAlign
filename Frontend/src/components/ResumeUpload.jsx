import React, { useState } from "react";

const API_URL = "https://job-matcher-ai.onrender.com";

export default function ResumeUpload({ setCandidateIds }) {
  const [files, setFiles] = useState([]);

  const handleFileChange = (e) => {
    setFiles([...e.target.files]); // store selected files
  };

  const handleUpload = async () => {
    if (files.length === 0) {
      alert("⚠️ Please select at least one resume file!");
      return;
    }

    const uploadedIds = [];

    for (const file of files) {
      const formData = new FormData();
      formData.append("file", file);

      try {
        const res = await fetch(`${API_URL}/upload_resume`, {
          method: "POST",
          body: formData,
        });
        const data = await res.json();
        uploadedIds.push(data.candidate_id);
      } catch (err) {
        console.error("Upload failed:", err);
        alert(`❌ Failed to upload ${file.name}`);
      }
    }

    setCandidateIds(uploadedIds);
    alert(`✅ Successfully uploaded ${uploadedIds.length} resume(s)!`);
  };

  return (
    <div className="p-4 border rounded-lg bg-gray-50">
      <h2 className="text-lg font-semibold mb-2">Upload Resumes</h2>
      <input
        type="file"
        multiple
        onChange={handleFileChange}
        className="mb-2"
      />
      <button
        onClick={handleUpload}
        className="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700"
      >
        Upload Selected Resumes
      </button>

      {files.length > 0 && (
        <ul className="mt-2 list-disc pl-5 text-sm text-gray-600">
          {files.map((f, idx) => (
            <li key={idx}>{f.name}</li>
          ))}
        </ul>
      )}
    </div>
  );
}
  