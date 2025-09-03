import pickle
from collections import Counter
from tqdm import tqdm
from .data_utils import SPECIAL_TOKENS, preprocess_text, load_spacy_model

class Vocabulary:
    def __init__(self):
        self.word2index = {}
        self.word2count = Counter()
        self.index2word = {}
        self.num_words = 0
        # Add special tokens first
        for token in SPECIAL_TOKENS:
            self.add_word(token)

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
        return self.word2index.get(word, self.word2index['<unk>'])

    def to_word(self, index):
        return self.index2word.get(index, '<unk>')

def build_vocab(data_pairs, min_word_count=5):
    """Builds vocabulary from a list of (article, summary) pairs"""
    print("Loading SpaCy model...")
    nlp = load_spacy_model()
    
    source_vocab = Vocabulary()
    target_vocab = Vocabulary()
    
    print("Processing data and building vocabulary...")
    for article, summary in tqdm(data_pairs):
        # Preprocess and add to vocab
        proc_article = preprocess_text(article, nlp)
        proc_summary = preprocess_text(summary, nlp)
        
        source_vocab.add_sentence(proc_article)
        target_vocab.add_sentence(proc_summary)
    
    print(f"Source Vocab Size: {source_vocab.num_words}")
    print(f"Target Vocab Size: {target_vocab.num_words}")
    
    return source_vocab, target_vocab

# Only run if this script is executed directly
if __name__ == '__main__':
    # Example for testing
    sample_data = [
        ("The cat sat on the mat. It was a nice day.", "Cat on mat."),
        ("Dogs are great pets. They are very loyal.", "Dogs are loyal.")
    ]
    src_vocab, trg_vocab = build_vocab(sample_data)
    print("Vocabulary building completed.")