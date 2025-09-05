from transformers import AutoTokenizer
from typing import Dict, List, Union
import torch

class SimpleTokenizer:
    
    def __init__(self, model_name: str = "facebook/bart-large"):
        
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        
        # Ensure we have a padding token
        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token
    
    def encode(self, text: str, max_length: int = 512, 
               truncation: bool = True, padding: bool = False) -> Dict[str, torch.Tensor]:
        
        return self.tokenizer(
            text,
            max_length=max_length,
            truncation=truncation,
            padding=padding,  
            return_tensors='pt',
            add_special_tokens=True
        )
    
    def decode(self, token_ids: torch.Tensor, skip_special_tokens: bool = True) -> str:
        return self.tokenizer.decode(
            token_ids,
            skip_special_tokens=skip_special_tokens,
            clean_up_tokenization_spaces=True
        )
    
    @property
    def vocab_size(self) -> int:
        return len(self.tokenizer)
    
    def get_vocab(self) -> Dict[str, int]:
        return self.tokenizer.get_vocab()
    
    def tokenize(self, text: str) -> List[str]:
        return self.tokenizer.tokenize(text)
    
    @property
    def pad_token_id(self) -> int:
        return self.tokenizer.pad_token_id
    
    @property
    def bos_token_id(self) -> int:
        return self.tokenizer.bos_token_id
    
    @property
    def eos_token_id(self) -> int:
        return self.tokenizer.eos_token_id