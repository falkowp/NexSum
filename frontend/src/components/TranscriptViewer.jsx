export default function TranscriptViewer({ transcript, processing }) {
  const handleDownload = () => {
    if (!transcript) return;
    
    const content = transcript.polished_transcript;
    const blob = new Blob([content], { type: "text/plain" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "transcript.txt";
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  if (!transcript && !processing) {
    return null;
  }

  return (
    <section className="transcript-section">
      <div className="section-header">
        <i className="fas fa-file-alt"></i>
        <h2>Transcript</h2>
      </div>
      
      <div className="section-content">
        {processing && !transcript ? (
          <div className="processing">
            <div className="spinner"></div>
          </div>
        ) : transcript ? (
          <div className="transcript-content">
            {transcript.polished_transcript}
          </div>
        ) : null}
      </div>
      
      {transcript && (
        <div className="section-actions">
          <button className="download-btn" onClick={handleDownload}>
            <i className="fas fa-download"></i> Download Transcript
          </button>
        </div>
      )}
    </section>
  );
}