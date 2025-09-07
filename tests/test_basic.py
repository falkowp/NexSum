import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.core.content_detector import ContentTypeDetector

def test_content_detection():
    print("🧪 TESTING CONTENT DETECTION")
    print("=" * 60)
    
    detector = ContentTypeDetector()
    
    # Test meeting content
    meeting_text = "John: Let's discuss the project. Sarah: I'll prepare the report by Friday."
    meeting_result = detector.detect_content_type(meeting_text)
    print(f"📋 Meeting text detected as: {meeting_result.content_type}")
    print(f"   Confidence: {meeting_result.confidence:.2f}")
    print(f"   Features: {meeting_result.features}")
    print()
    
    # Test academic content
    academic_text = "Neural networks and deep learning concepts include backpropagation and activation functions."
    academic_result = detector.detect_content_type(academic_text)
    print(f"🎓 Academic text detected as: {academic_result.content_type}")
    print(f"   Confidence: {academic_result.confidence:.2f}")
    print(f"   Features: {academic_result.features}")
    print()
    
    # Test book content
    book_text = "The protagonist journeyed through the ancient forest, following the mysterious prophecy."
    book_result = detector.detect_content_type(book_text)
    print(f"📚 Book text detected as: {book_result.content_type}")
    print(f"   Confidence: {book_result.confidence:.2f}")
    print(f"   Features: {book_result.features}")
    print()
    
    print("✅ Basic content detection test completed successfully!")
    return True

if __name__ == "__main__":
    test_content_detection()