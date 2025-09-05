"""
Utility functions for data processing and note formatting
"""

# Import main functions
from .notes import create_professional_notes
from .data_loader import load_sample_data

# Make available for import  
__all__ = [
    'create_professional_notes',
    'load_sample_data'
]

# Package metadata
__version__ = "1.0.0"