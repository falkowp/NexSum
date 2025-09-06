import sys
import os
import json

# Add src to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from src.text_processing.universal_processor import UniversalNotesGenerator

def test_meeting():
    print("=== MEETING TRANSCRIPT ===")
    meeting_text = """
    John: Okay team, let's start with the Q2 project status. Sarah, backend update?
    Sarah: We're at 80% completion but hitting database connection issues under load.
    Mike: What's the specific problem?
    Sarah: Connections timeout with 100+ concurrent users. We tried increasing pool size but no luck.
    John: Maybe server configuration issue? Mike, can you investigate?
    Mike: Yes, I'll check the server config and optimize by Friday.
    Sarah: I'll run more load tests to verify the issue.
    John: Good. Frontend status?
    Lisa: UI is 90% done, waiting on final API specs from backend.
    Sarah: API specs will be ready by Wednesday.
    John: Let's meet Thursday to review everything. Also, we need deployment strategy discussion.
    """
    
    generator = UniversalNotesGenerator()
    notes = generator.generate_notes(meeting_text)
    
    print(f"Detected type: {notes.get('content_type', 'unknown')}")
    
    if 'error' in notes:
        print(f"Error: {notes['error']}")
        return
    
    print(f"\n📝 Summary: {notes.get('summary', 'No summary')}")
    
    # Handle different content types
    if notes.get('content_type') == 'meeting':
        print(f"\n👥 Participants: {', '.join(notes.get('participants', []))}")
        
        print(f"\n✅ Action Items:")
        action_items = notes.get('action_items', [])
        if action_items:
            for i, action in enumerate(action_items, 1):
                print(f"   {i}. {action}")
        else:
            print("   No specific action items detected")
        
        print(f"\n🤝 Decisions:")
        decisions = notes.get('decisions', [])
        if decisions:
            for i, decision in enumerate(decisions, 1):
                print(f"   {i}. {decision}")
        else:
            print("   No specific decisions detected")
    else:
        print("\nAvailable fields:")
        for key, value in notes.items():
            if key != 'content_type' and value:
                print(f"{key}: {value}")
    
    print("\n" + "="*60)

def test_academic_lecture():
    print("\n=== ACADEMIC LECTURE ===")
    lecture_text = """
    Today we explore neural networks and deep learning. Neural networks are computing systems 
    inspired by biological neural networks. They consist of layers of interconnected nodes 
    that process and transform data. Deep learning refers to networks with many hidden layers.
    
    Learning Objectives:
    - Understand forward propagation where data moves through the network
    - Learn about backpropagation where errors are used to adjust weights
    - Study activation functions like ReLU that introduce non-linearity
    - Minimize loss functions through gradient descent optimization
    
    Key concepts include forward propagation, where data moves through the network, 
    and backpropagation, where errors are used to adjust weights. Activation functions 
    like ReLU introduce non-linearity.
    
    Applications include image recognition, natural language processing, and 
    autonomous systems. Recent advances in transformer architectures have 
    revolutionized language modeling with models like GPT and BERT.
    """
    
    generator = UniversalNotesGenerator()
    notes = generator.generate_notes(lecture_text)
    
    print(f"Detected type: {notes.get('content_type', 'unknown')}")
    
    if 'error' in notes:
        print(f"Error: {notes['error']}")
        return
    
    print(f"\n📝 Summary: {notes.get('summary', 'No summary')}")
    
    if notes.get('content_type') == 'academic':
        print(f"\n🧠 Key Concepts: {', '.join(notes.get('key_concepts', []))}")
        
        print(f"\n🎯 Learning Objectives:")
        objectives = notes.get('learning_objectives', [])
        if objectives and objectives[0] != "No specific learning objectives detected":
            for i, obj in enumerate(objectives, 1):
                print(f"   {i}. {obj}")
        else:
            print("   No specific learning objectives detected")
    else:
        print("\nAvailable fields:")
        for key, value in notes.items():
            if key != 'content_type' and value:
                print(f"{key}: {value}")
    
    print("\n" + "="*60)

def test_book_excerpt():
    print("\n=== BOOK EXCERPT ===")
    book_text = """
    Elizabeth stood at the edge of the forest, contemplating the mysterious events 
    that had unfolded. The ancient prophecy spoke of a chosen one who would restore 
    balance to the kingdom. 
    
    Themes of destiny and free will permeate this chapter. The symbolism of the 
    forest represents the unknown future, while the ancient oak tree symbolizes 
    wisdom and stability. Characters grapple with their roles in the coming conflict.
    
    Major plot points include Elizabeth's discovery of the hidden scroll and 
    her encounter with the mysterious stranger who warns of impending danger. 
    The chapter ends with her decision to embark on the perilous journey.
    """
    
    generator = UniversalNotesGenerator()
    notes = generator.generate_notes(book_text)
    
    print(f"Detected type: {notes.get('content_type', 'unknown')}")
    
    if 'error' in notes:
        print(f"Error: {notes['error']}")
        return
    
    print(f"\n📝 Summary: {notes.get('summary', 'No summary')}")
    
    if notes.get('content_type') == 'book':
        characters = notes.get('key_characters', [])
        print(f"\n👤 Key Characters: {', '.join(characters) if characters else 'No characters detected'}")
        
        print(f"\n🎭 Major Themes:")
        themes = notes.get('major_themes', [])
        if themes:
            for i, theme in enumerate(themes, 1):
                print(f"   {i}. {theme}")
        else:
            print("   No major themes detected")
    else:
        print("\nAvailable fields:")
        for key, value in notes.items():
            if key != 'content_type' and value:
                print(f"{key}: {value}")
    
    print("\n" + "="*60)

def test_general_content():
    print("\n=== GENERAL CONTENT ===")
    general_text = """
    The impact of artificial intelligence on modern society cannot be overstated. 
    AI technologies are transforming industries, creating new opportunities while 
    also presenting challenges. Ethical considerations around AI development 
    and deployment are increasingly important.
    
    Key areas affected include healthcare, where AI assists in diagnosis and 
    treatment planning; transportation, with autonomous vehicles; and education, 
    through personalized learning systems. The future will likely see even greater 
    integration of AI into daily life.
    """
    
    generator = UniversalNotesGenerator()
    notes = generator.generate_notes(general_text)
    
    print(f"Detected type: {notes.get('content_type', 'unknown')}")
    
    if 'error' in notes:
        print(f"Error: {notes['error']}")
        return
    
    print(f"\n📝 Summary: {notes.get('summary', 'No summary')}")
    
    print(f"\n🌟 Key Points:")
    key_points = notes.get('key_points', [])
    if key_points:
        for i, point in enumerate(key_points, 1):
            print(f"   {i}. {point}")
    else:
        print("   No key points detected")
    
    print("\n" + "="*60)

if __name__ == "__main__":
    test_meeting()
    test_academic_lecture()
    test_book_excerpt()
    test_general_content()