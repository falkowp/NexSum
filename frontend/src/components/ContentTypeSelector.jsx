import React from "react";

const TYPES = ["meeting", "academic", "book", "general"];

export default function ContentTypeSelector({ detectedType, confidence, evidence = [], selectedType, onChange, editable = true }) {

  return (
    <div className="content-type-card">
      <div className="content-type-header">
        <strong>Detected type:</strong>
        {editable ? (
          <select value={selectedType || detectedType || "general"} onChange={(e) => onChange(e.target.value)}>
            {TYPES.map((t) => (
              <option key={t} value={t}>{t}</option>
            ))}
          </select>
        ) : (
          <span className="detected-text">{detectedType || selectedType || 'general'}</span>
        )}
      </div>

      {evidence && evidence.length > 0 && (
        <div className="evidence">
          {evidence.slice(0, 6).map((ev, i) => (
            <span className="evidence-tag" key={i}>{ev}</span>
          ))}
        </div>
      )}
    </div>
  );
}
