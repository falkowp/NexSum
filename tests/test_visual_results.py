import sys
import os
import json
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.core.content_detector import ContentTypeDetector
from src.text_processing.meeting_processor import MeetingProcessor
from src.text_processing.academic_processor import AcademicProcessor
from src.text_processing.book_processor import BookProcessor
from src.text_processing.general_processor import GeneralProcessor

def print_result(title, result):
    print(f"\n{'='*60}")
    print(f"📊 {title}")
    print(f"{'='*60}")
    print(json.dumps(result, indent=2, ensure_ascii=False))

def test_meeting_processor():
    print("\n" + "🎯 TESTING MEETING PROCESSOR")
    print("=" * 60)
    
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
    
    processor = MeetingProcessor()
    result = processor.process(meeting_text)
    
    print_result("MEETING PROCESSING RESULTS", result.to_dict())
    return result

def test_academic_processor():
    print("\n" + "🎯 TESTING ACADEMIC PROCESSOR")
    print("=" * 60)
    
    academic_text = """
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
    
    processor = AcademicProcessor()
    result = processor.process(academic_text)
    
    print_result("ACADEMIC PROCESSING RESULTS", result.to_dict())
    return result

def test_book_processor():
    print("\n" + "🎯 TESTING BOOK PROCESSOR")
    print("=" * 60)
    
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
    
    Key characters include Elizabeth, the mysterious stranger, and the ancient oracle.
    The forest setting creates an atmosphere of mystery and anticipation.
    """
    
    processor = BookProcessor()
    result = processor.process(book_text)
    
    print_result("BOOK PROCESSING RESULTS", result.to_dict())
    return result

def test_general_processor():
    print("\n" + "🎯 TESTING GENERAL PROCESSOR")
    print("=" * 60)
    
    general_text = """
    The impact of artificial intelligence on modern society cannot be overstated. 
    AI technologies are transforming industries, creating new opportunities while 
    also presenting challenges. Ethical considerations around AI development 
    and deployment are increasingly important.
    
    Key areas affected include healthcare, where AI assists in diagnosis and 
    treatment planning; transportation, with autonomous vehicles; and education, 
    through personalized learning systems. The future will likely see even greater 
    integration of AI into daily life.
    
    Important considerations include data privacy, algorithmic bias, and the 
    need for responsible AI development practices. Organizations should prioritize 
    transparency and accountability in their AI systems.
    """
    
    processor = GeneralProcessor()
    result = processor.process(general_text)
    
    print_result("GENERAL PROCESSING RESULTS", result.to_dict())
    return result

def test_content_detection_accuracy():
    print("\n" + "🎯 TESTING CONTENT DETECTION ACCURACY")
    print("=" * 60)
    
    detector = ContentTypeDetector()
    
    test_cases = [
        ("Meeting text with speakers", "John: Let's meet. Sarah: I'll prepare docs.", "meeting"),
        ("Academic lecture", "Neural networks use backpropagation for learning.", "academic"),
        ("Book excerpt", "The hero journeyed through the ancient forest.", "book"),
        ("General content", "AI is transforming modern industries.", "general")
    ]
    
    print("Testing content detection on various inputs:")
    print("-" * 50)
    
    for description, text, expected_type in test_cases:
        result = detector.detect_content_type(text)
        status = "✅" if result.content_type == expected_type else "❌"
        print(f"{status} {description}:")
        print(f"   Expected: {expected_type}, Got: {result.content_type}")
        print(f"   Confidence: {result.confidence:.2f}")
        print()

if __name__ == "__main__":
    print("🚀 STARTING COMPREHENSIVE VISUAL TESTS")
    print("=" * 60)
    
    # Test content detection first
    from src.core.content_detector import ContentTypeDetector
    detector = ContentTypeDetector()
    
    # Run all tests
    test_content_detection_accuracy()
    test_meeting_processor()
    test_academic_processor()
    test_book_processor()
    test_general_processor()
    
    print("\n" + "🎉 ALL TESTS COMPLETED!")
    print("=" * 60)
    print("Check the results above to see what's working properly.")