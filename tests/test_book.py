import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from .src.processing.book_processor import BookProcessor

def test_book_processing():
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
    
    processor = BookProcessor()
    result = processor.process(book_text)
    
    assert result.content_type == 'book'
    assert 'key_characters' in result.metadata
    assert 'major_themes' in result.metadata
    print("Book processing test passed!")

if __name__ == "__main__":
    test_book_processing()