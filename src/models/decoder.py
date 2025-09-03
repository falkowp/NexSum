import torch
import torch.nn as nn
from .attention import Attention

class Decoder(nn.Module):
    def __init__(self, output_dim, embed_dim, hidden_dim, n_layers, dropout, attention):
        super().__init__()
        self.output_dim = output_dim
        self.attention = attention
        self.embedding = nn.Embedding(output_dim, embed_dim)
        self.lstm = nn.LSTM(embed_dim + hidden_dim * 2, hidden_dim, n_layers, dropout=dropout)
        self.fc_out = nn.Linear(hidden_dim * 3 + embed_dim, output_dim)
        self.dropout = nn.Dropout(dropout)
    
    def forward(self, input, hidden, cell, encoder_outputs, mask):
        # We'll implement this next!
        pass