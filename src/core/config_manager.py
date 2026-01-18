import json
from pathlib import Path
from typing import Dict, Any, List

from ..config.output_config import OutputConfig, OutputElement

class ConfigManager:
    
    def __init__(self, config_file: str = None):
        self.config_file = config_file
        self.custom_configs: Dict[str, Dict[str, OutputElement]] = {}
        
        if config_file and Path(config_file).exists():
            self.load_config(config_file)
    
    def load_config(self, config_file: str) -> None:
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                config_data = json.load(f)
            
            # Parse custom configurations
            for content_type, elements in config_data.get('output_elements', {}).items():
                self.custom_configs[content_type] = {}
                for elem_name, elem_config in elements.items():
                    self.custom_configs[content_type][elem_name] = OutputElement(
                        name=elem_name,
                        display_name=elem_config.get('display_name', elem_name),
                        priority=elem_config.get('priority', 99),
                        enabled=elem_config.get('enabled', True),
                        formatter=self._get_formatter(elem_config.get('formatter', 'list'))
                    )
                    
        except Exception as e:
            print(f"Warning: Could not load config file {config_file}: {e}")
    
    def _get_formatter(self, formatter_name: str):
        formatters = {
            'list': OutputConfig.list_formatter,
            'string': OutputConfig.string_formatter,
            'metadata': OutputConfig.metadata_formatter
        }
        return formatters.get(formatter_name, OutputConfig.list_formatter)
    
    def get_output_config(self, content_type: str) -> Dict[str, OutputElement]:
        if content_type in self.custom_configs:
            return self.custom_configs[content_type]
        return OutputConfig.get_config(content_type)
    
    def get_enabled_elements(self, content_type: str) -> List[OutputElement]:
        config = self.get_output_config(content_type)
        enabled_elements = [elem for elem in config.values() if elem.enabled]
        return sorted(enabled_elements, key=lambda x: x.priority)