from src.core.content_detector import ContentTypeDetector
from src.processing.meeting_processor import MeetingProcessor
from src.processing.academic_processor import AcademicProcessor
from src.processing.book_processor import BookProcessor
from src.processing.general_processor import GeneralProcessor
from src.utils.logger import setup_logger

class NexSum:
    """Main application class"""
    
    def __init__(self):
        self.logger = setup_logger("app.log")
        self.processors = {
            'meeting': MeetingProcessor(),
            'academic': AcademicProcessor(),
            'book': BookProcessor(),
            'general': GeneralProcessor()
        }
        self.detector = ContentTypeDetector()
    
    def process_text(self, text: str):
        """Process text and generate notes"""
        try:
            # Detect content type
            detection_result = self.detector.detect_content_type(text)
            
            # Get appropriate processor
            processor = self.processors.get(
                detection_result.content_type, 
                self.processors['general']
            )
            
            # Process text
            result = processor.process(text)
            
            return result.to_dict()
            
        except Exception as e:
            self.logger.error(f"Error processing text: {e}")
            return {"error": str(e), "content_type": "error"}