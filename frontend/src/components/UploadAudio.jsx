import { useState, useRef } from "react";
import api from "../api/client";
import TranscriptViewer from "./TranscriptViewer";
import SummaryViewer from "./SummaryViewer";
import ContentTypeSelector from "./ContentTypeSelector";

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
  const [error, setError] = useState("");  const [selectedType, setSelectedType] = useState(null);
  const [detected, setDetected] = useState(null);  const fileInputRef = useRef(null);
  const [isAwaitingConfirm, setIsAwaitingConfirm] = useState(false);
  const [isEditingType, setIsEditingType] = useState(false);
  const [cachedTranscriptText, setCachedTranscriptText] = useState(null);
  const [lastUsedType, setLastUsedType] = useState(null);

  const isSupportedFile = (file) => {
    if (!file) return false;
    const mime = file.type || "";
    return mime.startsWith("audio/") || mime === "video/mp4";
  };

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile) {
      if (!isSupportedFile(selectedFile)) {
        setError("Please select an audio file or MP4 video");
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
    setSelectedType(null);
    setDetected(null);
    setIsAwaitingConfirm(false);
    setCachedTranscriptText(null);
    setLastUsedType(null);
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
      onTranscribed(transcriptData);      // Store detected content type info
      const detectedType = transcriptData.content_type || null;
      const confidence = transcriptData.content_confidence || 0;
      const evidence = transcriptData.content_features?.evidence || transcriptData.content_features || [];
      setDetected({ detectedType, confidence, evidence });
      setSelectedType(detectedType);
      // Don't auto-summarize yet — ask user to confirm detected type first
      setStatus("detected");
      setIsAwaitingConfirm(true);
      setIsEditingType(false); // show plain text, not editable select
      // store transcript text for later summarization
      setCachedTranscriptText(transcriptData.polished_transcript);

    } catch (err) {
      console.error(err);
      setError("An unexpected error occurred");
      setStatus("error");
    } finally {
      onProcessingChange(false);
    }
  };

  // Summarize helper (used after user confirms detected type or requests regeneration)
  const doSummarize = async (type) => {
    if (!cachedTranscriptText) return;
    // When user confirms or triggers summarize, switch to non-editable text immediately
    setIsEditingType(false);
    setIsAwaitingConfirm(false);
    setStatus("summarizing");
    onProcessingChange(true);
    setError("");
    try {
      const summaryResp = await api.post("/summarize", {
        text: cachedTranscriptText,
        type: type || undefined,
      });

      if (summaryResp.data.success) {
        onSummarized(summaryResp.data.data.summary);
        setLastUsedType(type);
        // Update detected type to the one used for summary so UI shows it as text
        setDetected((d) => ({ ...(d || {}), detectedType: type }));
        setSelectedType(type);
        setStatus("complete");
      } else {
        setError(summaryResp.data.error || "Summarization failed");
        setStatus("error");
      }
    } catch (err) {
      console.error(err);
      setError("An unexpected error occurred during summarization");
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
    if (droppedFile && isSupportedFile(droppedFile)) {
      onFileSelect(droppedFile);
      setError("");
    } else {
      setError("Please drop an audio file or MP4 video");
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
                <h3>Drag & Drop your audio or MP4 video</h3>
                <p>Supported formats: MP3, WAV, M4A, MP4</p>
              </div>
              
              <input
                type="file"
                  accept=".mp3,.wav,.m4a,.mp4"
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
          <div style={{ gridColumn: '1 / -1' }}>
            <ContentTypeSelector
              detectedType={detected?.detectedType}
              confidence={detected?.confidence}
              evidence={detected?.evidence}
              selectedType={selectedType}
              onChange={setSelectedType}
              editable={isEditingType}
            />

            {/* Confirmation / regeneration controls */}
            {isAwaitingConfirm ? (
              <div className="content-confirm">
                <p style={{ marginTop: '0.6rem' }}>Is the detected type correct?</p>
                <div style={{ display: 'flex', gap: '0.5rem' }}>
                  <button className="confirm-btn" onClick={() => doSummarize(selectedType)}>
                    <i className="fas fa-check"></i> Yes — Summarize
                  </button>
                  <button className="change-btn" onClick={() => { setIsAwaitingConfirm(false); setIsEditingType(true); }}>
                    <i className="fas fa-edit"></i> No — Change Type
                  </button>
                </div>
              </div>
            ) : (
              <div className="regenerate-area">
                {!summary ? (
                  <button className={`summarize-btn ${!isAwaitingConfirm ? 'with-top' : ''}`} onClick={() => doSummarize(selectedType)}>
                    <i className="fas fa-play"></i> Summarize
                  </button>
                ) : selectedType !== lastUsedType ? (
                  <button className="regenerate-btn" onClick={() => doSummarize(selectedType)}>
                    <i className="fas fa-sync"></i> Regenerate Summary
                  </button>
                ) : null}
              </div>
            )}
          </div>

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