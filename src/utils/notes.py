"""
Professional note-taking formatter for academic and business use.
"""

from datetime import datetime
from typing import List

def extract_by_keywords(text: str, keywords: List[str], limit: int = 3, default_msg: str = "No specific items identified") -> str:
    """Extract sentences containing any of the keywords"""
    results = []
    sentences = text.split('. ')
    for sentence in sentences:
        lower_sentence = sentence.lower()
        if any(keyword in lower_sentence for keyword in keywords):
            results.append(sentence.strip())
    return '\n'.join(results[:limit]) or f"{default_msg} for: {', '.join(keywords[:3])}"

def create_professional_notes(original_text: str, summary: str) -> str:
    """
    Create structured, professional notes for any type of text.
    """
    words = original_text.split()
    text_type = detect_text_type(original_text)
    
    notes = "AI-GENERATED NOTES\n"
    notes += "=" * 60 + "\n\n"
    
    # Document header
    notes += f"Document Type: {text_type}\n"
    notes += f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n"
    
    # Executive Summary
    notes += "EXECUTIVE SUMMARY:\n"
    notes += "-" * 40 + "\n"
    notes += f"{summary}\n\n"
    
    # Key Points
    notes += "KEY POINTS:\n"
    notes += "-" * 40 + "\n"
    points = [p.strip() for p in summary.split('.') if p.strip() and len(p.strip()) > 10]
    for i, point in enumerate(points, 1):
        notes += f"{i}. {point}\n"
    notes += "\n"
    
    # Context-Aware Sections
    if is_meeting_text(original_text):
        notes += add_meeting_sections(original_text)
    elif is_academic_text(original_text):
        notes += add_academic_sections(original_text)
    else:
        notes += add_general_sections(original_text)
    
    # Statistics
    notes += "STATISTICS:\n"
    notes += "-" * 40 + "\n"
    notes += f"Original text length: {len(words)} words\n"
    notes += f"Summary length: {len(summary.split())} words\n"
    notes += f"Compression ratio: {len(words)/max(1, len(summary.split())):.1f}x\n"
    
    return notes

def detect_text_type(text: str) -> str:
    """Detect what kind of text this is."""
    text_lower = text.lower()
    
    if any(word in text_lower for word in ['meeting', 'discuss', 'agenda', 'minutes', 'action items']):
        return "Meeting Minutes"
    elif any(word in text_lower for word in ['chapter', 'theory', 'research', 'study', 'academic', 'paper']):
        return "Academic Text"
    elif any(word in text_lower for word in ['article', 'news', 'report', 'journal']):
        return "Article/Report"
    elif any(word in text_lower for word in ['book', 'novel', 'story']):
        return "Literature"
    else:
        return "General Document"

def is_meeting_text(text: str) -> bool:
    """Check if text appears to be meeting notes."""
    meeting_words = ['meeting', 'agenda', 'minutes', 'discussion', 'action', 'decision']
    return any(word in text.lower() for word in meeting_words)

def is_academic_text(text: str) -> bool:
    """Check if text appears to be academic."""
    academic_words = ['research', 'study', 'theory', 'hypothesis', 'methodology', 'results']
    return any(word in text.lower() for word in academic_words)

def add_meeting_sections(text: str) -> str:
    """Add meeting-specific sections."""
    sections = ""
    
    # Decisions Made
    sections += "DECISIONS MADE:\n"
    sections += "-" * 40 + "\n"
    sections += extract_meeting_decisions(text) + "\n\n"
    
    # Action Items
    sections += "ACTION ITEMS:\n"
    sections += "-" * 40 + "\n"
    sections += extract_action_items(text) + "\n\n"
    
    # Next Steps
    sections += "NEXT STEPS:\n"
    sections += "-" * 40 + "\n"
    sections += extract_next_steps(text) + "\n\n"
    
    return sections

def add_academic_sections(text: str) -> str:
    """Add academic-specific sections."""
    sections = ""
    
    # Key Concepts
    sections += "KEY CONCEPTS:\n"
    sections += "-" * 40 + "\n"
    sections += extract_academic_concepts(text) + "\n\n"
    
    # Important Findings
    sections += "IMPORTANT FINDINGS:\n"
    sections += "-" * 40 + "\n"
    sections += extract_findings(text) + "\n\n"
    
    # Definitions
    sections += "KEY DEFINITIONS:\n"
    sections += "-" * 40 + "\n"
    sections += extract_definitions(text) + "\n\n"
    
    return sections

def add_general_sections(text: str) -> str:
    """Add sections for general text."""
    sections = ""
    
    # Main Ideas
    sections += "MAIN IDEAS:\n"
    sections += "-" * 40 + "\n"
    sections += extract_main_ideas(text) + "\n\n"
    
    # Important Facts
    sections += "IMPORTANT FACTS:\n"
    sections += "-" * 40 + "\n"
    sections += extract_important_facts(text) + "\n\n"
    
    return sections

def extract_action_items(text: str) -> str:
    """Extract action items from text."""
    action_keywords = ['will', 'prepare', 'launch', 'aim to', 'schedule', 'priority']
    return extract_by_keywords(text, action_keywords, 5, "No specific action items")

def extract_meeting_decisions(text: str) -> str:
    """Extract decisions from meeting text."""
    decision_keywords = ['decided', 'agreed', 'concluded', 'set for', 'launch by', 'aim to']
    return extract_by_keywords(text, decision_keywords, 3, "No specific decisions")

def extract_next_steps(text: str) -> str:
    """Extract next steps from meeting text."""
    steps_keywords = ['schedule', 'demo', 'launch', 'next week', 'last week of', 'will be']
    return extract_by_keywords(text, steps_keywords, 3, "No specific next steps")

def extract_academic_concepts(text: str) -> str:
    """Extract academic concepts."""
    concept_keywords = ['concept', 'theory', 'model', 'framework', 'principle']
    return extract_by_keywords(text, concept_keywords, 3, "No specific concepts")

def extract_main_ideas(text: str) -> str:
    """Extract main ideas from general text."""
    # Simple implementation - returns first few sentences
    sentences = [s.strip() for s in text.split('. ') if s.strip()]
    return '\n'.join(sentences[:2]) or "No main ideas extracted."

def extract_important_facts(text: str) -> str:
    """Extract important facts."""
    fact_keywords = ['important', 'key', 'critical', 'essential', 'significant']
    return extract_by_keywords(text, fact_keywords, 3, "No specific facts")

def extract_findings(text: str) -> str:
    """Extract findings from academic text."""
    findings_keywords = ['found', 'discovered', 'results show', 'analysis indicates', 'concluded that']
    return extract_by_keywords(text, findings_keywords, 3, "No specific findings")

def extract_definitions(text: str) -> str:
    """Extract definitions from academic text."""
    definition_keywords = ['defined as', 'means', 'refers to', 'is called', 'known as']
    return extract_by_keywords(text, definition_keywords, 3, "No definitions")