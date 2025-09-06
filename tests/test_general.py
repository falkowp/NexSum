import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from .src.processing.general_processor import GeneralProcessor

def test_general_processing():
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
    
    processor = GeneralProcessor()
    result = processor.process(general_text)
    
    assert result.content_type == 'general'
    assert 'key_points' in result.metadata
    assert 'main_ideas' in result.metadata
    print("General processing test passed!")

if __name__ == "__main__":
    test_general_processing()