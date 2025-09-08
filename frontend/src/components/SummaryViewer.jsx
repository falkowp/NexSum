import { useState } from "react";
import api from "../api/client";

export default function SummaryViewer({ transcript }) {
  const [summary, setSummary] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  if (!transcript) return null;

  const handleSummarize = async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await api.post("/summarize", {
        text: transcript.polished_transcript,
        type: "general", // later make dropdown (academic/book/meeting)
      });
      if (res.data.success) {
        setSummary(res.data.summary);
      } else {
        setError(res.data.error || "Summarization failed");
      }
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="summary-viewer">
      <button onClick={handleSummarize} disabled={loading}>
        {loading ? "Summarizing..." : "Summarize Transcript"}
      </button>

      {error && <p style={{ color: "red" }}>{error}</p>}
      {summary && (
        <div>
          <h2>Summary</h2>
          <p>{summary}</p>
        </div>
      )}
    </div>
  );
}
