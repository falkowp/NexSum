#!/usr/bin/env python3
"""
Comprehensive test script for all content types.
"""

import sys
import json
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from main import SummarizerApp

def test_content_type(content_type, test_file, description):
    """Test a specific content type."""
    print(f"\n{'='*60}")
    print(f"TESTING {description.upper()}")
    print(f"{'='*60}")
    
    try:
        # Initialize summarizer
        summarizer = SummarizerApp()
        
        # Process the test file
        print(f"Processing {test_file}...")
        result = summarizer.process_file(test_file, content_type=content_type)
        
        if result['success']:
            print(f"✓ Successfully processed as {result['content_type']}")
            print(f"Summary length: {len(result['summary'])} characters")
            
            # Display summary
            print(f"\nSUMMARY:")
            print("-" * 40)
            print(result['summary'])
            
            # Display metadata
            print(f"\nMETADATA ELEMENTS:")
            print("-" * 40)
            for key, value in result.get('metadata', {}).items():
                if isinstance(value, list):
                    print(f"{key.replace('_', ' ').title()} ({len(value)} items):")
                    for i, item in enumerate(value[:3], 1):
                        print(f"  {i}. {item}")
                    if len(value) > 3:
                        print(f"  ... and {len(value) - 3} more")
                else:
                    print(f"{key.replace('_', ' ').title()}: {value}")
            
            return True
            
        else:
            print(f"✗ Error: {result.get('error')}")
            return False
            
    except Exception as e:
        print(f"✗ Exception: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_auto_detection():
    """Test auto-detection for all content types."""
    print(f"\n{'='*60}")
    print("TESTING AUTO-DETECTION")
    print(f"{'='*60}")
    
    test_files = {
        'academic': 'test_data/academic.txt',
        'book': 'test_data/book.txt', 
        'meeting': 'test_data/meeting.txt',
        'general': 'test_data/general.txt'
    }
    
    summarizer = SummarizerApp()
    
    results = {}
    for expected_type, test_file in test_files.items():
        print(f"\nTesting {expected_type} auto-detection...")
        
        try:
            # Read file content
            with open(test_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Test detection
            detected_type = summarizer.detect_content_type(content)
            results[expected_type] = detected_type
            
            print(f"  Expected: {expected_type}")
            print(f"  Detected: {detected_type}")
            print(f"  Match: {expected_type == detected_type}")
            
        except Exception as e:
            print(f"  Error: {e}")
            results[expected_type] = f"Error: {e}"
    
    return results

def test_output_formats():
    """Test different output formats."""
    print(f"\n{'='*60}")
    print("TESTING OUTPUT FORMATS")
    print(f"{'='*60}")
    
    test_file = 'test_data/meeting.txt'
    output_files = {
        'text': 'test_output_meeting.txt',
        'markdown': 'test_output_meeting.md',
        'json': 'test_output_meeting.json'
    }
    
    summarizer = SummarizerApp()
    
    for format_name, output_file in output_files.items():
        print(f"\nTesting {format_name} format...")
        
        try:
            result = summarizer.process_file(
                test_file, 
                output_file, 
                content_type='meeting',
                output_format=format_name
            )
            
            if result['success']:
                print(f"  ✓ {format_name} output saved to {output_file}")
            else:
                print(f"  ✗ Error: {result.get('error')}")
                
        except Exception as e:
            print(f"  ✗ Exception: {e}")

def main():
    """Run all tests."""
    print("NexSum Content Type Testing")
    print("=" * 60)
    
    # Create test data directory if it doesn't exist
    test_data_dir = Path('test_data')
    test_data_dir.mkdir(exist_ok=True)
    
    # Check if test files exist
    test_files = {
        'academic': 'test_data/academic.txt',
        'book': 'test_data/book.txt',
        'meeting': 'test_data/meeting.txt', 
        'general': 'test_data/general.txt'
    }
    
    missing_files = []
    for content_type, file_path in test_files.items():
        if not Path(file_path).exists():
            missing_files.append(file_path)
    
    if missing_files:
        print("Missing test files. Please create the following files:")
        for file in missing_files:
            print(f"  - {file}")
        return
    
    # Run individual content type tests
    test_cases = [
        ('academic', 'test_data/academic.txt', 'Academic Content'),
        ('book', 'test_data/book.txt', 'Book Content'),
        ('meeting', 'test_data/meeting.txt', 'Meeting Content'),
        ('general', 'test_data/general.txt', 'General Content')
    ]
    
    results = {}
    for content_type, test_file, description in test_cases:
        success = test_content_type(content_type, test_file, description)
        results[content_type] = 'PASS' if success else 'FAIL'
    
    # Run auto-detection test
    auto_results = test_auto_detection()
    
    # Run output format test
    test_output_formats()
    
    # Print summary
    print(f"\n{'='*60}")
    print("TEST SUMMARY")
    print(f"{'='*60}")
    
    print("\nIndividual Tests:")
    for content_type, result in results.items():
        print(f"  {content_type:12}: {result}")
    
    print("\nAuto-detection Results:")
    for expected, detected in auto_results.items():
        status = "✓" if expected == detected else "✗"
        print(f"  {expected:12}: {detected} {status}")
    
    print(f"\nOutput files created:")
    for format_name in ['txt', 'md', 'json']:
        file_path = f'test_output_meeting.{format_name}'
        if Path(file_path).exists():
            print(f"  - {file_path}")
    
    # Calculate success rate
    total_tests = len(results) + len(auto_results)
    passed_tests = (
        sum(1 for r in results.values() if r == 'PASS') +
        sum(1 for expected, detected in auto_results.items() if expected == detected)
    )
    
    print(f"\nOverall: {passed_tests}/{total_tests} tests passed")
    
    if passed_tests == total_tests:
        print("🎉 All tests passed successfully!")
        return 0
    else:
        print("❌ Some tests failed.")
        return 1

if __name__ == "__main__":
    exit(main())