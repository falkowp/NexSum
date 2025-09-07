"""
Configuration for output elements by content type.
"""

from typing import Dict, List, Any, Callable
from dataclasses import dataclass

@dataclass
class OutputElement:
    """Configuration for a single output element."""
    name: str
    display_name: str
    priority: int
    formatter: Callable[[Any], str]
    enabled: bool = True

class OutputConfig:
    """Configuration for output elements by content type."""
    
    # Base formatters
    @staticmethod
    def list_formatter(items: List[str]) -> str:
        if not items:
            return "None identified"
        return "\n".join([f"  • {item}" for item in items])
    
    @staticmethod
    def string_formatter(text: str) -> str:
        return text if text else "Not available"
    
    @staticmethod
    def metadata_formatter(metadata: Dict[str, Any]) -> str:
        if not metadata:
            return "No metadata available"
        return json.dumps(metadata, indent=2, ensure_ascii=False)
    
    # Content type configurations
    MEETING_CONFIG: Dict[str, OutputElement] = {
        'summary': OutputElement(
            name='summary',
            display_name='Meeting Summary',
            priority=1,
            formatter=string_formatter
        ),
        'participants': OutputElement(
            name='participants',
            display_name='Participants',
            priority=2,
            formatter=list_formatter
        ),
        'action_items': OutputElement(
            name='action_items',
            display_name='Action Items',
            priority=3,
            formatter=list_formatter
        ),
        'decisions': OutputElement(
            name='decisions',
            display_name='Key Decisions',
            priority=4,
            formatter=list_formatter
        ),
        'key_points': OutputElement(
            name='key_points',
            display_name='Key Discussion Points',
            priority=5,
            formatter=list_formatter
        )
    }
    
    ACADEMIC_CONFIG: Dict[str, OutputElement] = {
        'summary': OutputElement(
            name='summary',
            display_name='Lecture Summary',
            priority=1,
            formatter=string_formatter
        ),
        'key_concepts': OutputElement(
            name='key_concepts',
            display_name='Key Concepts',
            priority=2,
            formatter=list_formatter
        ),
        'learning_objectives': OutputElement(
            name='learning_objectives',
            display_name='Learning Objectives',
            priority=3,
            formatter=list_formatter
        ),
        'main_topics': OutputElement(
            name='main_topics',
            display_name='Main Topics',
            priority=4,
            formatter=list_formatter
        ),
        'key_definitions': OutputElement(
            name='key_definitions',
            display_name='Key Definitions',
            priority=5,
            formatter=list_formatter
        )
    }
    
    BOOK_CONFIG: Dict[str, OutputElement] = {
        'summary': OutputElement(
            name='summary',
            display_name='Book Summary',
            priority=1,
            formatter=string_formatter
        ),
        'key_characters': OutputElement(
            name='key_characters',
            display_name='Key Characters',
            priority=2,
            formatter=list_formatter
        ),
        'major_themes': OutputElement(
            name='major_themes',
            display_name='Major Themes',
            priority=3,
            formatter=list_formatter
        ),
        'plot_points': OutputElement(
            name='plot_points',
            display_name='Plot Points',
            priority=4,
            formatter=list_formatter
        ),
        'setting': OutputElement(
            name='setting',
            display_name='Setting',
            priority=5,
            formatter=list_formatter
        )
    }
    
    GENERAL_CONFIG: Dict[str, OutputElement] = {
        'summary': OutputElement(
            name='summary',
            display_name='Summary',
            priority=1,
            formatter=string_formatter
        ),
        'key_points': OutputElement(
            name='key_points',
            display_name='Key Points',
            priority=2,
            formatter=list_formatter
        ),
        'main_ideas': OutputElement(
            name='main_ideas',
            display_name='Main Ideas',
            priority=3,
            formatter=list_formatter
        ),
        'actionable_items': OutputElement(
            name='actionable_items',
            display_name='Actionable Items',
            priority=4,
            formatter=list_formatter
        )
    }
    
    @classmethod
    def get_config(cls, content_type: str) -> Dict[str, OutputElement]:
        """Get output configuration for content type."""
        configs = {
            'meeting': cls.MEETING_CONFIG,
            'academic': cls.ACADEMIC_CONFIG,
            'book': cls.BOOK_CONFIG,
            'general': cls.GENERAL_CONFIG
        }
        return configs.get(content_type, cls.GENERAL_CONFIG)
    
    @classmethod
    def get_enabled_elements(cls, content_type: str) -> List[OutputElement]:
        """Get enabled output elements for content type, sorted by priority."""
        config = cls.get_config(content_type)
        enabled_elements = [elem for elem in config.values() if elem.enabled]
        return sorted(enabled_elements, key=lambda x: x.priority)