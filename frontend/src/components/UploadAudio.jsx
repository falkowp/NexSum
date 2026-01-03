import { useState, useRef } from "react";
import api from "../api/client";
import TranscriptViewer from "./TranscriptViewer";
import SummaryViewer from "./SummaryViewer";

export default function UploadAudio({ 
  onTranscribed, 
  onSummarized, 
  onProcessingChange, 
  onFileSelect, 
  file, 
  transcript, 
  summary, 
  processing,
  onReset 
}) {
  const [_status, setStatus] = useState("idle"); 
  const [error, setError] = useState("");
  const fileInputRef = useRef(null);

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile) {
      if (!selectedFile.type.startsWith('audio/')) {
        setError("Please select an audio file");
        return;
      }
      onFileSelect(selectedFile);
      setError("");
    }
  };

  const removeFile = () => {
    onFileSelect(null);
    onTranscribed(null);
    onSummarized(null);
    setStatus("idle");
    setError("");
    if (fileInputRef.current) {
      fileInputRef.current.value = "";
    }
  };

  const handleUpload = async () => {
    if (!file) return;
    
    setStatus("uploading");
    onProcessingChange(true);
    setError("");
    
    const formData = new FormData();
    formData.append("audio", file);

    try {
      setStatus("transcribing");
      const response = await api.post("/transcribe", formData, {
        headers: { "Content-Type": "multipart/form-data" },
        onUploadProgress: () => {
        }
      });

      if (!response.data.success) {
        setError(response.data.error || "Transcription failed");
        setStatus("error");
        onProcessingChange(false);
        return;
      }

      const transcriptData = response.data.data;
      onTranscribed(transcriptData);

      setStatus("summarizing");
      const summaryResp = await api.post("/summarize", {
        text: transcriptData.polished_transcript,
      });

      if (summaryResp.data.success) {
        onSummarized(summaryResp.data.data.summary);
        setStatus("complete");
      } else {
        setError(summaryResp.data.error || "Summarization failed");
        setStatus("error");
      }
    } catch (err) {
      console.error(err);
      setError("An unexpected error occurred");
      setStatus("error");
    } finally {
      onProcessingChange(false);
    }
  };

  const handleDragOver = (e) => {
    e.preventDefault();
    if (!transcript && !summary) {
      e.currentTarget.classList.add("active");
    }
  };

  const handleDragLeave = (e) => {
    e.preventDefault();
    e.currentTarget.classList.remove("active");
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.currentTarget.classList.remove("active");
    
    if (transcript && summary) return;
    
    const droppedFile = e.dataTransfer.files[0];
    if (droppedFile && droppedFile.type.startsWith('audio/')) {
      onFileSelect(droppedFile);
      setError("");
    } else {
      setError("Please drop an audio file");
    }
  };

  return (
    <section className="upload-section">
      <h2>Upload Audio File</h2>
      
      {!transcript && !summary ? (
        <div 
          className={`upload-area ${file ? "has-file" : ""}`}
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          onDrop={handleDrop}
        >
          {!file ? (
            <>
              <div className="upload-icon">
                <i className="fas fa-cloud-upload-alt"></i>
              </div>
              
              <div className="upload-text">
                <h3>Drag & Drop your audio file</h3>
                <p>Supported formats: MP3, WAV, M4A</p>
              </div>
              
              <input
                type="file"
                accept=".mp3,.wav,.m4a"
                onChange={handleFileChange}
                className="file-input"
                id="file-input"
                ref={fileInputRef}
              />
              <label htmlFor="file-input" className="file-label">
                <i className="fas fa-file-audio"></i> Select File
              </label>
            </>
          ) : (
            <>
              <div className="selected-file">
                <div className="file-info">
                  <i className="fas fa-file-audio"></i>
                  <span>{file.name}</span>
                </div>
                <button className="remove-file" onClick={removeFile}>
                  <i className="fas fa-times"></i>
                </button>
              </div>

              {processing && (
                <div className="processing-status">
                  <div className="spinner"></div>
                  <p className="processing-text">Processing, this may take a while...</p>
                </div>
              )}
            </>
          )}
        </div>
      ) : (
        <div className="results-container">
          <TranscriptViewer transcript={transcript} processing={processing} />
          <SummaryViewer summary={summary} processing={processing} />
          
          <div className="reset-section">
            <p className="reset-warning">
              <i className="fas fa-exclamation-triangle"></i> This action will delete the current transcript and notes
            </p>
            <button className="reset-btn" onClick={onReset}>
              <i className="fas fa-plus"></i> Upload Next File
            </button>
          </div>
        </div>
      )}

      {error && (
        <div className="error-message">
          <i className="fas fa-exclamation-circle"></i> {error}
        </div>
      )}

      {file && !transcript && !summary && !processing && (
        <button 
          onClick={handleUpload} 
          className="upload-btn"
        >
          <i className="fas fa-gear"></i> Process File
        </button>
      )}
    </section>
  );
}