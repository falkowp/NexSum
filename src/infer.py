import torch
from src.models.transformers import SimpleTransformer
from src.data.tokenizer import SimpleTokenizer
from src.utils.notes import create_professional_notes

class SimpleInference:
    def __init__(self, model_path=None):
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.tokenizer = SimpleTokenizer()
        
        self.model = SimpleTransformer(
            vocab_size=self.tokenizer.vocab_size,
            d_model=256,
            n_layers=3,
            n_heads=4,
            ff_dim=1024,
            max_len=256
        ).to(self.device)
        
        if model_path:
            self.model.load_state_dict(torch.load(model_path, map_location=self.device))
        
        self.model.eval()
    
    def generate_summary(self, text, max_length=100):
        # Encode source
        inputs = self.tokenizer.encode(text)
        src = inputs['input_ids'].to(self.device)
        
        # Create source mask
        src_mask = self.create_src_mask(src)
        
        # Encode source
        with torch.no_grad():
            src_emb = self.model.embedding(src) * math.sqrt(self.model.d_model)
            src_pos_encoding = self.model._create_pos_encoding(src.size(1), self.model.d_model).to(src.device)
            src_emb = src_emb + src_pos_encoding
            memory = self.model.encoder_layers(src_emb, src_mask=src_mask)
        
        # Generate target autoregressively
        target_ids = torch.ones(1, 1).fill_(self.tokenizer.bos_token_id).long().to(self.device)
        
        for _ in range(max_length):
            # Create target mask
            tgt_mask = self.create_tgt_mask(target_ids.size(1))
            
            with torch.no_grad():
                output = self.model.decoder_layers(
                    self.model.embedding(target_ids) * math.sqrt(self.model.d_model),
                    memory,
                    tgt_mask=tgt_mask,
                    memory_mask=src_mask
                )
                next_token = output[:, -1, :].argmax(-1).unsqueeze(-1)
                
                target_ids = torch.cat([target_ids, next_token], dim=1)
                
                if next_token.item() == self.tokenizer.eos_token_id:
                    break
        
        return self.tokenizer.decode(target_ids[0])
        
def main():
    from transformers import pipeline
    
    print("Generating demo summary...")
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    
    sample_text = """
    [John] Team, we need to discuss Q4 results. Sales were strong but marketing costs increased.
    [Sarah] Yes, we spent 20% more on digital ads but saw 30% higher conversion rates.
    [Mike] The new AI recommendation system is driving most of this growth.
    [Lisa] However, customer support tickets have also increased by 15%.
    [John] Let's allocate more resources to support and continue the marketing strategy.
    """
    
    summary = summarizer(sample_text, max_length=100, min_length=30)[0]['summary_text']
    
    notes = create_professional_notes(sample_text, summary)
    
    print("\n" + "="*80)
    print(notes)
    print("="*80)

if __name__ == "__main__":
    main()