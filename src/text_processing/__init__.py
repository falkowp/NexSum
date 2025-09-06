from .academic_processor import AcademicProcessor
from .base_processor import TextPreprocessor
from .book_processor import BookProcessor
from .general_processor import GeneralProcessor
from .meeting_processor import MeetingProcessor

__all__ = [
    'BaseProcessor', 
    'MeetingProcessor', 
    'AcademicProcessor', 
    'BookProcessor', 
    'GeneralProcessor']