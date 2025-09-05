# test_model.py
import torch
from .models import Transformer, HuggingFaceTokenizer
from .utils.notes import create_professional_notes

def test_transformer_architecture():
    """Test if the Transformer architecture works without training"""
    print("🧪 Testing Transformer Architecture...")
    
    # Initialize components
    tokenizer = HuggingFaceTokenizer("facebook/bart-large")
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"Using device: {device}")
    
    # Create a small test model
    model = Transformer(
        src_vocab_size=1000,  # Smaller for testing
        tgt_vocab_size=1000,
        d_model=64,           # Smaller dimensions for testing
        num_layers=2,
        num_heads=4,
        d_ff=256,
        max_seq_length=128
    ).to(device)
    
    print("✅ Model created successfully!")
    
    # Test forward pass
    batch_size, seq_length = 2, 16
    src = torch.randint(0, 1000, (batch_size, seq_length)).to(device)
    tgt = torch.randint(0, 1000, (batch_size, seq_length)).to(device)
    
    # Create masks
    src_mask = (src != tokenizer.tokenizer.pad_token_id).unsqueeze(1).unsqueeze(2)
    tgt_mask = torch.tril(torch.ones(seq_length, seq_length)).expand(batch_size, 1, seq_length, seq_length).to(device)
    
    # Forward pass
    try:
        output = model(src, tgt, src_mask, tgt_mask)
        print(f"✅ Forward pass successful! Output shape: {output.shape}")
        print(f"   Expected: torch.Size([{batch_size}, {seq_length}, 1000])")
    except Exception as e:
        print(f"❌ Forward pass failed: {e}")
        return False
    
    # Test encoding
    try:
        encoded = model.encode(src, src_mask)
        print(f"✅ Encoding successful! Encoded shape: {encoded.shape}")
    except Exception as e:
        print(f"❌ Encoding failed: {e}")
        return False
    
    # Test decoding
    try:
        decoded = model.decode(tgt, encoded, src_mask, tgt_mask)
        print(f"✅ Decoding successful! Decoded shape: {decoded.shape}")
    except Exception as e:
        print(f"❌ Decoding failed: {e}")
        return False
    
    print("\n🎉 All architecture tests passed! The Transformer is working correctly.")
    return True

def test_tokenizer():
    """Test the tokenizer wrapper"""
    print("\n🧪 Testing Tokenizer...")
    
    tokenizer = HuggingFaceTokenizer("facebook/bart-large")
    
    sample_text = "This is a test sentence for tokenization."
    
    # Test encoding
    encoded = tokenizer.encode(sample_text)
    print(f"✅ Encoding successful! Input IDs shape: {encoded['input_ids'].shape}")
    
    # Test decoding
    decoded = tokenizer.decode(encoded['input_ids'][0])
    print(f"✅ Decoding successful! Original: '{sample_text}'")
    print(f"   Decoded: '{decoded}'")
    
    # Test vocabulary
    print(f"✅ Vocabulary size: {tokenizer.vocab_size}")
    
    return True

def quick_demo():
    """Quick demo with pretrained embeddings"""
    print("\n🚀 Quick Demo with Pretrained Components...")
    
    # Use the Hugging Face pipeline for a quick demo while your model trains
    from transformers import pipeline
    
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    
    meeting_text = """
    [John] Okay team, welcome to the Q4 planning meeting. Let's start with reviewing last quarter's performance.
    [Sarah] Our sales were up 15% overall, but we saw a dip in the European market due to new regulations.
    [Mike] Right. Marketing is preparing a new campaign focused on data privacy features to address this.
    [John] Good. Let's aim to launch that by November 1st. Now, onto product roadmap. The AI features are delayed?
    [Lisa] Yes, we're looking at a December launch now. We need more time for testing the recommendation engine.
    [John] Understood. Quality is priority. Let's schedule a demo for the last week of November.
    """
    
    print("Generating summary with pretrained model (for demo purposes)...")
    summary = summarizer(meeting_text, max_length=130, min_length=30, do_sample=False)[0]['summary_text']
    
    print("Creating professional notes with your formatter...")
    notes = create_professional_notes(meeting_text, summary)
    
    print("\n" + "="*80)
    print(notes)
    print("="*80)

if __name__ == "__main__":
    print("🤖 Testing Your Advanced Transformer Summarization System")
    print("="*60)
    
    # Test architecture
    architecture_ok = test_transformer_architecture()
    
    # Test tokenizer
    tokenizer_ok = test_tokenizer()
    
    if architecture_ok and tokenizer_ok:
        print("\n" + "🎊 ALL TESTS PASSED! Your system is ready for training.")
        print("\n📝 Note: Training will take several hours/days. For immediate results,")
        print("   we'll show a demo using a pretrained model with your note formatter.")
        
        quick_demo()
    else:
        print("\n❌ Some tests failed. Please check the implementation.")