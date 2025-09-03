import spacy
import pickle
from collections import defaultdict, Counter
import torch
from tqdm import tqdm
import os

# Special tokens
SOS_TOKEN = '<sos>'
EOS_TOKEN = '<eos>'
PAD_TOKEN = '<pad>'
UNK_TOKEN = '<unk>'
SPECIAL_TOKENS = [PAD_TOKEN, SOS_TOKEN, EOS_TOKEN, UNK_TOKEN]

class Vocabulary:
    def __init__(self):
        self.word2index = {}
        self.word2count = Counter()
        self.index2word = {}
        self.num_words = 0
        self.add_word(PAD_TOKEN)  # PAD_TOKEN must be index 0
        self.add_word(SOS_TOKEN)
        self.add_word(EOS_TOKEN)
        self.add_word(UNK_TOKEN)

    def add_word(self, word):
        if word not in self.word2index:
            self.word2index[word] = self.num_words
            self.index2word[self.num_words] = word
            self.num_words += 1
        self.word2count[word] += 1

    def add_sentence(self, sentence):
        for word in sentence.split():
            self.add_word(word)

    def to_index(self, word):
        return self.word2index.get(word, self.word2index[UNK_TOKEN])

    def to_word(self, index):
        return self.index2word.get(index, UNK_TOKEN)

def preprocess_text(text, nlp):
    """Cleans and tokenizes text using SpaCy"""
    doc = nlp(text.lower().strip())
    tokens = [token.lemma_ for token in doc if not token.is_stop and not token.is_punct and not token.is_space]
    return " ".join(tokens)

def build_vocab(data_pairs, min_word_count=5):
    """Builds vocabulary from a list of (article, summary) pairs"""
    print("Loading SpaCy model...")
    nlp = spacy.load("en_core_web_sm", disable=["parser", "ner"])
    
    source_vocab = Vocabulary()
    target_vocab = Vocabulary()
    
    print("Processing data and building vocabulary...")
    for article, summary in tqdm(data_pairs):
        # Preprocess and add to vocab
        proc_article = preprocess_text(article, nlp)
        proc_summary = preprocess_text(summary, nlp)
        
        source_vocab.add_sentence(proc_article)
        target_vocab.add_sentence(proc_summary)
    
    # Optional: Filter words based on min_word_count
    print(f"Initial Source Vocab Size: {source_vocab.num_words}")
    print(f"Initial Target Vocab Size: {target_vocab.num_words}")
    
    return source_vocab, target_vocab

if __name__ == '__main__':
    # Example for testing
    sample_data = [
        ("The cat sat on the mat. It was a nice day.", "Cat on mat."),
        ("Dogs are great pets. They are very loyal.", "Dogs are loyal.")
    ]
    src_vocab, trg_vocab = build_vocab(sample_data)
    print("Source vocab size:", src_vocab.num_words)
    print("Target vocab size:", trg_vocab.num_words)
    
    # Get the absolute path to the processed directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    processed_dir = os.path.join(current_dir, '..', 'data', 'processed')
    
    # Create the directory if it doesn't exist
    os.makedirs(processed_dir, exist_ok=True)
    
    # Save the vocabs with absolute paths
    src_vocab_path = os.path.join(processed_dir, 'src_vocab.pkl')
    trg_vocab_path = os.path.join(processed_dir, 'trg_vocab.pkl')
    
    with open(src_vocab_path, 'wb') as f:
        pickle.dump(src_vocab, f)
    with open(trg_vocab_path, 'wb') as f:
        pickle.dump(trg_vocab, f)
    print(f"Vocabularies saved to {processed_dir}")