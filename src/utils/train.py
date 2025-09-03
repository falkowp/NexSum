import torch
from torch.utils.data import Dataset, DataLoader
import pickle
import os
from tqdm import tqdm
from .data_utils import SOS_TOKEN, EOS_TOKEN, PAD_TOKEN, preprocess_text, load_spacy_model

class TextDataset(Dataset):
    def __init__(self, data_pairs, source_vocab, target_vocab, max_len=100):
        self.data = []
        self.source_vocab = source_vocab
        self.target_vocab = target_vocab
        self.max_len = max_len
        self.nlp = load_spacy_model()
        
        print("Processing dataset...")
        for article, summary in tqdm(data_pairs):
            # Preprocess the SAME way as during vocab building!
            proc_article = preprocess_text(article, self.nlp)
            proc_summary = preprocess_text(summary, self.nlp)
            
            # Convert preprocessed text to indices
            article_indices = self.text_to_indices(proc_article, source_vocab)
            summary_indices = self.text_to_indices(proc_summary, target_vocab)
            
            # Skip empty sequences
            if len(article_indices) == 0 or len(summary_indices) == 0:
                continue
                
            # Add SOS and EOS tokens to summary
            summary_indices = [target_vocab.to_index(SOS_TOKEN)] + summary_indices + [target_vocab.to_index(EOS_TOKEN)]
            
            # Truncate if too long
            if len(article_indices) > max_len:
                article_indices = article_indices[:max_len]
            if len(summary_indices) > max_len:
                summary_indices = summary_indices[:max_len]
                
            self.data.append({
                'article': article_indices,
                'article_len': len(article_indices),
                'summary': summary_indices,
                'summary_len': len(summary_indices)
            })
    
    def text_to_indices(self, text, vocab):
        """Convert preprocessed text to indices"""
        tokens = text.split()
        return [vocab.to_index(token) for token in tokens]
    
    def __len__(self):
        return len(self.data)
    
    def __getitem__(self, idx):
        return self.data[idx]

def collate_fn(batch):
    """Custom collate function to pad sequences in each batch"""
    articles = [item['article'] for item in batch]
    articles_len = torch.tensor([item['article_len'] for item in batch])
    summaries = [item['summary'] for item in batch]
    summaries_len = torch.tensor([item['summary_len'] for item in batch])
    
    # Pad sequences to the longest in the batch
    articles_padded = torch.nn.utils.rnn.pad_sequence(
        [torch.tensor(art) for art in articles],
        batch_first=True,
        padding_value=0  # PAD_TOKEN index
    )
    
    summaries_padded = torch.nn.utils.rnn.pad_sequence(
        [torch.tensor(summ) for summ in summaries],
        batch_first=True,
        padding_value=0  # PAD_TOKEN index
    )
    
    return {
        'articles': articles_padded,
        'articles_len': articles_len,
        'summaries': summaries_padded,
        'summaries_len': summaries_len
    }

# Test function should be separate
def test_dataset():
    """Test the dataset functionality"""
    test_data = [
        ("The quick brown fox jumps over the lazy dog", "Fox jumps over dog"),
        ("Cats are independent animals that enjoy sleeping", "Cats enjoy sleeping"),
        ("Programming computers requires logical thinking and problem solving skills", "Programming needs logic")
    ]
    
    # Build vocab from test data
    from .preprocess import build_vocab
    src_vocab, trg_vocab = build_vocab(test_data)
    
    # Create and test dataset
    dataset = TextDataset(test_data, src_vocab, trg_vocab, max_len=20)
    dataloader = DataLoader(dataset, batch_size=2, shuffle=True, collate_fn=collate_fn)
    
    for batch in dataloader:
        print("Article shape:", batch['articles'].shape)
        print("Article lengths:", batch['articles_len'])
        print("Summary shape:", batch['summaries'].shape)
        print("Summary lengths:", batch['summaries_len'])
        break

if __name__ == '__main__':
    test_dataset()