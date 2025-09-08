import { useState } from "react";
import UploadAudio from "../components/UploadAudio";
import TranscriptViewer from "../components/TranscriptViewer";
import SummaryViewer from "../components/SummaryViewer";

export default function Home() {
  const [transcript, setTranscript] = useState(null);

  return (
    <div className="home">
      <h1>NexSum — Note Taking App</h1>
      <UploadAudio onTranscribed={setTranscript} />
      <TranscriptViewer transcript={transcript} />
      <SummaryViewer transcript={transcript} />
    </div>
  );
}
