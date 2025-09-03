import spacy
import torch

# Special tokens (define in one place only)
SOS_TOKEN = '<sos>'
EOS_TOKEN = '<eos>'
PAD_TOKEN = '<pad>'
UNK_TOKEN = '<unk>'
SPECIAL_TOKENS = [PAD_TOKEN, SOS_TOKEN, EOS_TOKEN, UNK_TOKEN]

def preprocess_text(text, nlp):
    """Cleans and tokenizes text using SpaCy"""
    doc = nlp(text.lower().strip())
    tokens = [token.lemma_ for token in doc if not token.is_stop and not token.is_punct and not token.is_space]
    return " ".join(tokens)

def load_spacy_model():
    """Load SpaCy model with disabled components for efficiency"""
    return spacy.load("en_core_web_sm", disable=["parser", "ner"])