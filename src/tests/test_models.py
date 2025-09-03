import torch
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from models import Encoder, Attention

def test_encoder():
    print("Testing Encoder...")
    encoder = Encoder(vocab_size=1000, embed_dim=64, hidden_dim=128, n_layers=1, dropout=0.0)
    dummy_input = torch.tensor([[1, 2, 3, 0, 0], [4, 5, 6, 7, 8]])
    dummy_lengths = torch.tensor([3, 5])
    
    outputs, hidden = encoder(dummy_input, dummy_lengths)
    print(f"Encoder outputs: {outputs.shape}, hidden: {hidden.shape}")
    return outputs, hidden

def test_attention(encoder_outputs):
    print("Testing Attention...")
    attention = Attention(hidden_dim=128)
    decoder_hidden = torch.randn(2, 128)  # Batch size 2, hidden dim 128
    mask = torch.tensor([[1, 1, 1, 0, 0], [1, 1, 1, 1, 1]])
    
    attention_weights = attention(decoder_hidden, encoder_outputs, mask)
    print(f"Attention weights: {attention_weights.shape}")
    print(f"Attention sums: {attention_weights.sum(dim=1)}")
    return attention_weights

if __name__ == '__main__':
    print("Testing model components...\n")
    encoder_outputs, hidden = test_encoder()
    print()
    attention_weights = test_attention(encoder_outputs)
    print("\n✓ All tests passed!")