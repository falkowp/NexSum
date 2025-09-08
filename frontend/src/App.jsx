import { useState } from "react";
import UploadAudio from "./components/UploadAudio";
import "./App.css";

export default function App() {
  const [transcript, setTranscript] = useState(null);
  const [summary, setSummary] = useState(null);
  const [processing, setProcessing] = useState(false);
  const [file, setFile] = useState(null);

  const handleReset = () => {
    setTranscript(null);
    setSummary(null);
    setFile(null);
  };

  return (
    <div className="app">
      <header className="app-header">
        <h1><i className="fas fa-microphone-alt"></i> NexSum</h1>
        <p>Professional Audio Transcription & Summarization</p>
      </header>

      <main className="app-main">
        <UploadAudio 
          onTranscribed={setTranscript} 
          onSummarized={setSummary}
          onProcessingChange={setProcessing}
          onFileSelect={setFile}
          file={file}
          transcript={transcript}
          summary={summary}
          processing={processing}
          onReset={handleReset}
        />
      </main>

      <footer className="app-footer">
        <p>© 2023 NexSum — Professional Audio Processing</p>
      </footer>
    </div>
  );
}