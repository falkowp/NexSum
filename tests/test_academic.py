import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from .src.processing.academic_processor import AcademicProcessor

def test_academic_processing():
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
    """
    
    processor = AcademicProcessor()
    result = processor.process(academic_text)
    
    assert result.content_type == 'academic'
    assert 'key_concepts' in result.metadata
    assert 'learning_objectives' in result.metadata
    print("Academic processing test passed!")

if __name__ == "__main__":
    test_academic_processing()