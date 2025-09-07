"""
Output formatting utilities.
"""

import json
from typing import Dict, Any, List
from pathlib import Path

from config.output_config import OutputConfig

class OutputFormatter:
    """Format output results for different content types."""
    
    @staticmethod
    def format_result(result: Dict[str, Any], format_type: str = 'text') -> str:
        """
        Format processing result.
        
        Args:
            result: Processing result dictionary
            format_type: Output format ('text', 'json', 'markdown')
            
        Returns:
            Formatted output string
        """
        if format_type == 'json':
            return OutputFormatter._format_json(result)
        elif format_type == 'markdown':
            return OutputFormatter._format_markdown(result)
        else:
            return OutputFormatter._format_text(result)
    
    @staticmethod
    def _format_text(result: Dict[str, Any]) -> str:
        """Format as plain text."""
        if not result.get('success'):
            return f"ERROR: {result.get('error', 'Unknown error')}"
        
        content_type = result['content_type']
        output_lines = []
        
        # Get enabled output elements for this content type
        elements = OutputConfig.get_enabled_elements(content_type)
        
        for element in elements:
            element_name = element.name
            display_name = element.display_name
            formatter = element.formatter
            
            if element_name in result.get('metadata', {}):
                value = result['metadata'][element_name]
            elif element_name in result:
                value = result[element_name]
            else:
                continue
            
            formatted_value = formatter(value)
            
            output_lines.append(f"{display_name}:\n{formatted_value}\n")
        
        return "\n".join(output_lines)
    
    @staticmethod
    def _format_markdown(result: Dict[str, Any]) -> str:
        """Format as Markdown."""
        if not result.get('success'):
            return f"# ERROR\n\n{result.get('error', 'Unknown error')}"
        
        content_type = result['content_type']
        output_lines = [f"# {content_type.title()} Analysis\n"]
        
        elements = OutputConfig.get_enabled_elements(content_type)
        
        for element in elements:
            element_name = element.name
            display_name = element.display_name
            formatter = element.formatter
            
            if element_name in result.get('metadata', {}):
                value = result['metadata'][element_name]
            elif element_name in result:
                value = result[element_name]
            else:
                continue
            
            formatted_value = formatter(value)
            
            output_lines.append(f"## {display_name}\n")
            if isinstance(value, list):
                for item in value:
                    output_lines.append(f"- {item}")
            else:
                output_lines.append(f"{formatted_value}")
            output_lines.append("")
        
        return "\n".join(output_lines)
    
    @staticmethod
    def _format_json(result: Dict[str, Any]) -> str:
        """Format as JSON."""
        return json.dumps(result, indent=2, ensure_ascii=False)
    
    @staticmethod
    def save_output(result: Dict[str, Any], output_path: str, format_type: str = 'text') -> None:
        """
        Save formatted output to file.
        
        Args:
            result: Processing result
            output_path: Output file path
            format_type: Output format
        """
        formatted_output = OutputFormatter.format_result(result, format_type)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(formatted_output)