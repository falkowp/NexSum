"""
Model components for the Transformer summarization system
"""

# Import main classes
from .transformer import SimpleTransformer
from .tokenizer import SimpleTokenizer

# Make available for import
__all__ = [
    'SimpleTransformer',
    'SimpleTokenizer'
]

# Package metadata
__version__ = "1.0.0"