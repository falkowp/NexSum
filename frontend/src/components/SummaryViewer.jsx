export default function SummaryViewer({ summary, processing }) {
  const handleDownload = () => {
    if (!summary) return;
    
    const blob = new Blob([summary], { type: "text/plain" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "notes.txt";
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  if (!summary && !processing) {
    return null;
  }

  return (
    <section className="summary-section">
      <div className="section-header">
        <i className="fas fa-sticky-note"></i>
        <h2>Notes</h2>
      </div>
      
      <div className="section-content">
        {processing && !summary ? (
          <div className="processing">
            <div className="spinner"></div>
          </div>
        ) : summary ? (
          <div className="summary-content">
            {summary}
          </div>
        ) : null}
      </div>
      
      {summary && (
        <div className="section-actions">
          <button className="download-btn" onClick={handleDownload}>
            <i className="fas fa-download"></i> Download Notes
          </button>
        </div>
      )}
    </section>
  );
}