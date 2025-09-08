import { useState } from "react";
import api from "../api/client";

export default function UploadAudio({ onTranscribed }) {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append("audio", file);

    setLoading(true);
    setError(null);
    try {
      const res = await api.post("/transcribe", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      if (res.data.success) {
        onTranscribed(res.data.data);
      } else {
        setError(res.data.error || "Transcription failed");
      }
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="upload-audio">
      <input type="file" accept="audio/*" onChange={handleUpload} />
      {loading && <p>Transcribing...</p>}
      {error && <p style={{ color: "red" }}>{error}</p>}
    </div>
  );
}
