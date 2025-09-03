import torch
import torch.nn as nn
from .encoder import Encoder
from .attention import Attention
from .decoder import Decoder

class Seq2Seq(nn.Module):
    def __init__(self, encoder, decoder, src_pad_idx, device):
        super().__init__()
        self.encoder = encoder
        self.decoder = decoder
        self.src_pad_idx = src_pad_idx
        self.device = device
    
    def create_mask(self, src):
        return (src != self.src_pad_idx)
    
    def forward(self, src, src_len, trg, teacher_forcing_ratio=0.5):
        # We'll implement this after decoder
        pass