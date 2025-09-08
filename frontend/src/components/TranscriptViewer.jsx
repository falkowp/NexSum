export default function TranscriptViewer({ transcript }) {
  if (!transcript) return null;

  return (
    <div className="transcript-viewer">
      <h2>Transcript</h2>
      <pre>{transcript.raw_transcript}</pre>
      <h3>Polished</h3>
      <p>{transcript.polished_transcript}</p>
    </div>
  );
}
