import torch
from torch.utils.data import Dataset
from typing import List, Tuple, Dict, Any

class SummaryDataset(Dataset):
    
    def __init__(self, data_pairs: List[Tuple[str, str]], tokenizer: Any, max_length: int = 512):
        self.data = data_pairs
        self.tokenizer = tokenizer
        self.max_length = max_length
    
    def __len__(self) -> int:
        return len(self.data)
    
    def __getitem__(self, idx: int) -> Dict[str, torch.Tensor]:
        src_text, tgt_text = self.data[idx]
        
        try:
            src_enc = self.tokenizer.encode(
                src_text, 
                max_length=self.max_length,
                truncation=True,
                padding=False
            )
            tgt_enc = self.tokenizer.encode(
                tgt_text,
                max_length=self.max_length // 2,
                truncation=True,
                padding=False
            )
        except Exception as e:
            raise ValueError(f"Tokenization failed for sample {idx}: {e}")
        
        return {
            'src_ids': src_enc['input_ids'].squeeze(0), 
            'tgt_ids': tgt_enc['input_ids'].squeeze(0),
            'src_text': src_text,
            'tgt_text': tgt_text
        }

def collate_fn(batch: List[Dict[str, torch.Tensor]]) -> Dict[str, torch.Tensor]:

    src_ids = [item['src_ids'] for item in batch]
    tgt_ids = [item['tgt_ids'] for item in batch]
    src_texts = [item['src_text'] for item in batch]
    tgt_texts = [item['tgt_text'] for item in batch]
    
    max_src_len = max(len(ids) for ids in src_ids)
    max_tgt_len = max(len(ids) for ids in tgt_ids)
    
    padded_src_ids = torch.stack([
        torch.cat([ids, torch.zeros(max_src_len - len(ids), dtype=torch.long)]) 
        for ids in src_ids
    ])
    
    padded_tgt_ids = torch.stack([
        torch.cat([ids, torch.zeros(max_tgt_len - len(ids), dtype=torch.long)]) 
        for ids in tgt_ids
    ])
    
    return {
        'src_ids': padded_src_ids,
        'tgt_ids': padded_tgt_ids,
        'src_text': src_texts,
        'tgt_text': tgt_texts
    }