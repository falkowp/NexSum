import torch
import torch.nn as nn
import torch.nn.functional as F
import math
from typing import Optional, Tuple

class SimpleTransformer(nn.Module):
    
    def __init__(self, vocab_size: int, d_model: int = 512, n_layers: int = 4, 
                 n_heads: int = 8, ff_dim: int = 2048, max_len: int = 512, 
                 dropout: float = 0.1):
        super().__init__()
        self.d_model = d_model
        self.max_len = max_len
        self.vocab_size = vocab_size
        
        self.embedding = nn.Embedding(vocab_size, d_model)
        
        self.encoder_layers = nn.ModuleList([
            nn.TransformerEncoderLayer(
                d_model=d_model,
                nhead=n_heads,
                dim_feedforward=ff_dim,
                dropout=dropout,
                batch_first=True,
                activation='relu'
            )
            for _ in range(n_layers)
        ])
        
        self.decoder_layers = nn.ModuleList([
            nn.TransformerDecoderLayer(
                d_model=d_model,
                nhead=n_heads,
                dim_feedforward=ff_dim,
                dropout=dropout,
                batch_first=True,
                activation='relu'
            )
            for _ in range(n_layers)
        ])
        
        self.fc_out = nn.Linear(d_model, vocab_size)
        self.dropout = nn.Dropout(dropout)
        
        self._init_weights()
    
    def _init_weights(self):
        for p in self.parameters():
            if p.dim() > 1:
                nn.init.xavier_uniform_(p)
    
    def _create_pos_encoding(self, seq_len: int, d_model: int) -> torch.Tensor:
        if not hasattr(self, 'pos_encoding') or self.pos_encoding.size(1) < seq_len:
            position = torch.arange(0, seq_len, dtype=torch.float).unsqueeze(1)
            div_term = torch.exp(
                torch.arange(0, d_model, 2).float() * (-math.log(10000.0) / d_model)
            )
            
            pos_encoding = torch.zeros(seq_len, d_model)
            pos_encoding[:, 0::2] = torch.sin(position * div_term)
            pos_encoding[:, 1::2] = torch.cos(position * div_term)
            
            self.pos_encoding = pos_encoding.unsqueeze(0)  
        
        return self.pos_encoding[:, :seq_len, :]
    
    def create_src_mask(self, src: torch.Tensor, pad_token_id: int = 0) -> torch.Tensor:
        src_mask = (src != pad_token_id)
        return src_mask
    
    def create_tgt_mask(self, tgt_len: int) -> torch.Tensor:
        tgt_mask = torch.tril(torch.ones(tgt_len, tgt_len)).bool()
        return tgt_mask
    
    def forward(self, src: torch.Tensor, tgt: torch.Tensor, 
                src_mask: Optional[torch.Tensor] = None, 
                tgt_mask: Optional[torch.Tensor] = None) -> torch.Tensor:
        batch_size, src_len = src.size()
        _, tgt_len = tgt.size()
        
        src_emb = self.embedding(src) * math.sqrt(self.d_model)
        tgt_emb = self.embedding(tgt) * math.sqrt(self.d_model)
        
        src_pos_encoding = self._create_pos_encoding(src_len, self.d_model).to(src.device)
        tgt_pos_encoding = self._create_pos_encoding(tgt_len, self.d_model).to(tgt.device)
        
        src_emb = src_emb + src_pos_encoding
        tgt_emb = tgt_emb + tgt_pos_encoding
        
        src_emb = self.dropout(src_emb)
        tgt_emb = self.dropout(tgt_emb)
        
        memory = src_emb
        for layer in self.encoder_layers:
            memory = layer(memory, src_key_padding_mask=~src_mask if src_mask is not None else None)
        
        output = tgt_emb
        for layer in self.decoder_layers:
            output = layer(
                output, 
                memory, 
                tgt_mask=tgt_mask,
                tgt_key_padding_mask=~tgt_mask if tgt_mask is not None else None,
                memory_key_padding_mask=~src_mask if src_mask is not None else None
            )
        
        return self.fc_out(output)
    
    def count_parameters(self) -> int:
        return sum(p.numel() for p in self.parameters() if p.requires_grad)
    
    def get_config(self) -> dict:
        return {
            'vocab_size': self.vocab_size,
            'd_model': self.d_model,
            'n_layers': len(self.encoder_layers),
            'n_heads': self.encoder_layers[0].self_attn.num_heads,
            'ff_dim': self.encoder_layers[0].linear1.out_features,
            'max_len': self.max_len,
            'dropout': self.dropout.p,
            'parameters': self.count_parameters()
        }