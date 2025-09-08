import { useState } from "react";
import api from "../api/client";

export default function UploadAudio() {
  const [file, setFile] = useState(null);
  const [polishedTranscript, setPolishedTranscript] = useState("");
  const [summary, setSummary] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleUpload = async () => {
    if (!file) return;
    setLoading(true);
    setError("");

    const formData = new FormData();
    formData.append("audio", file);

    try {
      // 1️⃣ Transcription
      const response = await api.post("/transcribe", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });

      if (!response.data.success) {
        setError(response.data.error || "Transcription failed");
        setLoading(false);
        return;
      }

      const polished = response.data.data.polished_transcript;
      setPolishedTranscript(polished);

      // 2️⃣ Summarization
      const summaryResp = await api.post("/summarize", {
        text: polished,
      });

      if (summaryResp.data.success) {
        setSummary(summaryResp.data.data.summary);
      } else {
        setError(summaryResp.data.error || "Summarization failed");
      }
    } catch (err) {
      console.error(err);
      setError("An unexpected error occurred");
    } finally {
      setLoading(false);
    }
  };

  // Function to download text
  const handleDownload = (text, filename) => {
    const blob = new Blob([text], { type: "text/plain" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = filename;
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div style={{ maxWidth: "600px", margin: "0 auto", padding: "1rem" }}>
      <h2>Upload Audio for Polished Transcript & Summary</h2>

      <input
        type="file"
        accept=".mp3,.wav,.m4a"
        onChange={handleFileChange}
      />
      <button onClick={handleUpload} disabled={loading || !file}>
        {loading ? "Processing..." : "Upload & Process"}
      </button>

      {error && <p style={{ color: "red" }}>{error}</p>}

      {loading && <p>Processing audio... Please wait ⏳</p>}

      {polishedTranscript && (
        <div style={{ marginTop: "1rem" }}>
          <h3>Polished Transcript:</h3>
          <div style={{ maxHeight: "200px", overflowY: "auto", border: "1px solid #ccc", padding: "0.5rem" }}>
            {polishedTranscript}
          </div>
          <button onClick={() => handleDownload(polishedTranscript, "transcript.txt")}>
            Download Transcript
          </button>
        </div>
      )}

      {summary && (
        <div style={{ marginTop: "1rem" }}>
          <h3>Summary:</h3>
          <div style={{ maxHeight: "150px", overflowY: "auto", border: "1px solid #ccc", padding: "0.5rem" }}>
            {summary}
          </div>
          <button onClick={() => handleDownload(summary, "summary.txt")}>
            Download Summary
          </button>
        </div>
      )}
    </div>
  );
}
