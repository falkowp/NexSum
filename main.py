"""
Main entry point for the summarizer module.
Handles text summarization pipeline from input to output with configurable output elements.
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Optional, Dict, Any, List

from src.core.content_detector import ContentTypeDetector
from src.core.processor import BaseProcessor
from src.text_processing.academic_processor import AcademicProcessor
from src.text_processing.book_processor import BookProcessor
from src.text_processing.general_processor import GeneralProcessor
from src.text_processing.meeting_processor import MeetingProcessor
from src.utils.validators import validate_text
from src.utils.helpers import clean_text
from src.utils.output_formatter import OutputFormatter
from src.core.config_manager import ConfigManager

class SummarizerApp:
    """Main application class for the summarizer functionality."""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the summarizer application.
        """
        self.config = config or {}
        
        # Initialize content detector
        self.content_detector = ContentTypeDetector()
        
        # Initialize processors
        self.processors: Dict[str, BaseProcessor] = {
            'academic': AcademicProcessor(),
            'book': BookProcessor(),
            'general': GeneralProcessor(),
            'meeting': MeetingProcessor()
        }
        
        # Initialize config manager
        self.config_manager = ConfigManager(self.config.get('config_file'))
    
    def detect_content_type(self, text: str) -> str:
        """
        Detect the content type of the input text.
        """
        try:
            detection_result = self.content_detector.detect_content_type(text)
            print(f"Content type detected: {detection_result.content_type} "
                  f"(confidence: {detection_result.confidence:.2f})")
            return detection_result.content_type
        except Exception as e:
            print(f"Content detection failed: {e}. Using 'general' as fallback.")
            return 'general'
    
    def get_processor(self, content_type: str) -> BaseProcessor:
        """
        Get the appropriate processor for the content type.
        """
        processor = self.processors.get(content_type)
        if not processor:
            print(f"No processor found for content type '{content_type}'. Using general processor.")
            return self.processors['general']
        return processor
    
    def summarize_text(self, text: str, content_type: Optional[str] = None) -> Dict[str, Any]:
        """
        Process text through the complete summarization pipeline.
        """
        try:
            # Validate and clean input text
            validated_text = validate_text(text)
            cleaned_text = clean_text(validated_text)
            
            # Detect content type if not provided
            if content_type is None:
                content_type = self.detect_content_type(cleaned_text)
            
            print(f"Processing as {content_type} content...")
            
            # Get appropriate processor
            processor = self.get_processor(content_type)
            
            # Process the text
            result = processor.process(cleaned_text)
            
            # Convert result to dictionary for easier handling
            return {
                'content_type': result.content_type,
                'summary': result.summary,
                'metadata': result.metadata,
                'success': True,
                'raw_text_length': len(text)
            }
            
        except Exception as e:
            print(f"Error processing text: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'content_type': content_type or 'unknown'
            }
    
    def process_file(self, input_path: str, output_path: Optional[str] = None, 
                    content_type: Optional[str] = None, output_format: str = 'text') -> Dict[str, Any]:
        """
        Process a text file through the summarization pipeline.
        """
        try:
            # Read input file
            input_path_obj = Path(input_path)
            if not input_path_obj.exists():
                raise FileNotFoundError(f"Input file not found: {input_path}")
            
            print(f"Reading input file: {input_path}")
            with open(input_path, 'r', encoding='utf-8') as f:
                text_content = f.read()
            
            # Process the text
            result = self.summarize_text(text_content, content_type)
            
            # Save output if output_path provided
            if output_path and result['success']:
                self._save_output(result, output_path, output_format)
            
            return result
            
        except Exception as e:
            print(f"Error processing file {input_path}: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'content_type': content_type or 'unknown'
            }
    
    def _save_output(self, result: Dict[str, Any], output_path: str, format_type: str = 'text') -> None:
        """Save processing results to output file."""
        try:
            OutputFormatter.save_output(result, output_path, format_type)
            print(f"Output saved to: {output_path} (format: {format_type})")
        except Exception as e:
            print(f"Error saving output to {output_path}: {str(e)}")
            raise
    
    def get_available_elements(self, content_type: str) -> List[Dict[str, Any]]:
        """
        Get available output elements for content type.
        """
        elements = self.config_manager.get_enabled_elements(content_type)
        return [{
            'name': elem.name,
            'display_name': elem.display_name,
            'priority': elem.priority,
            'enabled': elem.enabled
        } for elem in elements]
    
    def list_content_types(self) -> List[Dict[str, Any]]:
        """
        List all available content types and their processors.
        """
        content_types = []
        for content_type, processor in self.processors.items():
            content_types.append({
                'type': content_type,
                'processor': processor.__class__.__name__,
                'available': True
            })
        return content_types

def main():
    """Command-line interface for the summarizer."""
    parser = argparse.ArgumentParser(
        description='NexSum - Advanced Text Summarization Tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Process with auto-detection
  python src/summarizer_main.py input.txt
  
  # Process with specific content type
  python src/summarizer_main.py input.txt --type meeting
  
  # Save output to markdown file
  python src/summarizer_main.py input.txt --output summary.md --format markdown
  
  # Use custom configuration
  python src/summarizer_main.py input.txt --config config/custom_output.json
  
  # List available content types
  python src/summarizer_main.py --list-types
  
  # Show available output elements for a type
  python src/summarizer_main.py --list-elements meeting
        """
    )
    
    parser.add_argument('input', nargs='?', help='Input text file path')
    parser.add_argument('-o', '--output', help='Output file path (optional)')
    parser.add_argument('-t', '--type', 
                       choices=['academic', 'book', 'general', 'meeting', 'auto'],
                       default='auto',
                       help='Content type (default: auto-detect)')
    parser.add_argument('-f', '--format', 
                       choices=['text', 'markdown', 'json'],
                       default='text',
                       help='Output format (default: text)')
    parser.add_argument('-c', '--config', 
                       help='Custom configuration file path')
    parser.add_argument('--list-types', action='store_true',
                       help='List available content types and exit')
    parser.add_argument('--list-elements', 
                       choices=['academic', 'book', 'general', 'meeting'],
                       help='List available output elements for content type and exit')
    parser.add_argument('-v', '--verbose', action='store_true', 
                       help='Verbose output (show more details)')
    parser.add_argument('--version', action='version', version='NexSum 1.0.0')
    
    args = parser.parse_args()
    
    # Handle list commands
    if args.list_types:
        summarizer = SummarizerApp()
        content_types = summarizer.list_content_types()
        print("Available Content Types:")
        print("=" * 40)
        for ct in content_types:
            print(f"{ct['type']:12} - {ct['processor']}")
        return 0
    
    if args.list_elements:
        summarizer = SummarizerApp()
        elements = summarizer.get_available_elements(args.list_elements)
        print(f"Available Output Elements for '{args.list_elements}':")
        print("=" * 50)
        for elem in elements:
            print(f"{elem['name']:20} - {elem['display_name']} (priority: {elem['priority']})")
        return 0
    
    # Validate input file
    if not args.input:
        parser.error("Input file is required")
    
    input_path = Path(args.input)
    if not input_path.exists():
        parser.error(f"Input file not found: {args.input}")
    
    # Initialize and run summarizer
    summarizer = SummarizerApp()
    
    try:
        # Determine content type
        content_type = None if args.type == 'auto' else args.type
        
        result = summarizer.process_file(
            args.input, 
            args.output, 
            content_type, 
            args.format
        )
        
        if result['success']:
            print(f"\n✓ Summary completed successfully!")
            print(f"Content Type: {result['content_type']}")
            print(f"Input Length: {result.get('raw_text_length', 0)} characters")
            
            # Display summary in console if no output file specified
            if not args.output:
                print(f"\nSummary:\n{'-' * 40}")
                print(result['summary'])
                
                if args.verbose:
                    print(f"\nMetadata:\n{'-' * 40}")
                    for key, value in result.get('metadata', {}).items():
                        if isinstance(value, list):
                            print(f"{key.replace('_', ' ').title()}:")
                            for item in value[:3]:  # Show first 3 items
                                print(f"  • {item}")
                            if len(value) > 3:
                                print(f"  • ... and {len(value) - 3} more")
                        else:
                            print(f"{key.replace('_', ' ').title()}: {value}")
        else:
            print(f"\n✗ Error: {result.get('error', 'Unknown error')}")
            return 1
            
    except KeyboardInterrupt:
        print("\n✗ Operation cancelled by user")
        return 1
    except Exception as e:
        print(f"\n✗ Fatal error: {str(e)}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())