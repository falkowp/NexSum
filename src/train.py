import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from tqdm import tqdm
import time
import os
import numpy as np

from .models.transformer import SimpleTransformer
from .data.tokenizer import SimpleTokenizer
from .data.dataset import SummaryDataset, collate_fn
from .utils.real_data_loader import load_sample_data, load_validation_data

def create_dataloaders(tokenizer, batch_size=2):
    train_data = load_sample_data()
    val_data = load_validation_data()
    
    print(f"Training with {len(train_data)} real business articles")
    print(f"Validating with {len(val_data)} examples")
    
    train_dataset = SummaryDataset(train_data, tokenizer)
    val_dataset = SummaryDataset(val_data, tokenizer)
    
    train_loader = DataLoader(
        train_dataset, 
        batch_size=batch_size, 
        shuffle=True,
        collate_fn=collate_fn
    )
    val_loader = DataLoader(
        val_dataset, 
        batch_size=batch_size, 
        shuffle=False,
        collate_fn=collate_fn
    )
    
    return train_loader, val_loader

def validate_model(model, val_loader, criterion, device, pad_token_id):
    model.eval()
    total_loss = 0
    
    with torch.no_grad():
        for batch in val_loader:
            src_ids = batch['src_ids'].to(device)
            tgt_ids = batch['tgt_ids'].to(device)
            
            src_mask = model.create_src_mask(src_ids, pad_token_id)
            tgt_mask = model.create_tgt_mask(tgt_ids.size(1) - 1)
            
            output = model(src_ids, tgt_ids[:, :-1], src_mask=src_mask, tgt_mask=tgt_mask)
            loss = criterion(
                output.contiguous().view(-1, output.size(-1)),
                tgt_ids[:, 1:].contiguous().view(-1)
            )
            total_loss += loss.item()
    
    model.train()
    return total_loss / len(val_loader)

def train_model():
    print("Starting Business Transformer Training with REAL DATA")
    print("=" * 60)
    
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"Using device: {device}")
    
    tokenizer = SimpleTokenizer()
    model = SimpleTransformer(
        vocab_size=tokenizer.vocab_size,
        d_model=256,
        n_layers=3,
        n_heads=4,
        ff_dim=1024,
        max_len=512,
        dropout=0.2
    ).to(device)
    
    print(f"Model parameters: {sum(p.numel() for p in model.parameters()):,}")
    
    optimizer = optim.Adam(
        model.parameters(), 
        lr=0.00001,  
        betas=(0.9, 0.98), 
        eps=1e-9,
        weight_decay=0.001
    )
    
    scheduler = optim.lr_scheduler.StepLR(optimizer, step_size=3, gamma=0.9)
    
    criterion = nn.CrossEntropyLoss(ignore_index=tokenizer.pad_token_id)
    
    train_loader, val_loader = create_dataloaders(tokenizer, batch_size=2)
    
    model.train()
    num_epochs = 30
    best_val_loss = float('inf')
    patience_counter = 0
    patience = 8 
    
    train_losses = []
    val_losses = []
    
    for epoch in range(num_epochs):
        epoch_loss = 0
        start_time = time.time()
        
        progress_bar = tqdm(train_loader, desc=f'Epoch {epoch+1}/{num_epochs}')
        
        for batch in progress_bar:
            src_ids = batch['src_ids'].to(device)
            tgt_ids = batch['tgt_ids'].to(device)
            
            src_mask = model.create_src_mask(src_ids, tokenizer.pad_token_id)
            tgt_mask = model.create_tgt_mask(tgt_ids.size(1) - 1)
            
            optimizer.zero_grad()
            output = model(src_ids, tgt_ids[:, :-1], src_mask=src_mask, tgt_mask=tgt_mask)
            
            loss = criterion(
                output.contiguous().view(-1, output.size(-1)),
                tgt_ids[:, 1:].contiguous().view(-1)
            )
            
            loss.backward()
            
            torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
            
            optimizer.step()
            
            epoch_loss += loss.item()
            progress_bar.set_postfix({
                'loss': f'{loss.item():.4f}',
                'avg_loss': f'{epoch_loss/(progress_bar.n+1):.4f}'
            })
        
        scheduler.step()
        current_lr = scheduler.get_last_lr()[0]
        
        avg_train_loss = epoch_loss / len(train_loader)
        avg_val_loss = validate_model(model, val_loader, criterion, device, tokenizer.pad_token_id)
        
        train_losses.append(avg_train_loss)
        val_losses.append(avg_val_loss)
        
        epoch_time = time.time() - start_time
        
        print(f'Epoch {epoch+1} - Train Loss: {avg_train_loss:.4f}, Val Loss: {avg_val_loss:.4f}, LR: {current_lr:.2e}, Time: {epoch_time:.1f}s')
        
        if avg_val_loss < best_val_loss:
            best_val_loss = avg_val_loss
            patience_counter = 0
            os.makedirs('models', exist_ok=True)
            torch.save(model.state_dict(), 'models/best_transformer.pth')
            print(f"New best model saved! Val Loss: {avg_val_loss:.4f}")
        else:
            patience_counter += 1
            print(f"No improvement for {patience_counter} epochs")
            
            if patience_counter >= patience:
                print(f"Early stopping triggered after {epoch+1} epochs")
                break
        
        if (epoch + 1) % 3 == 0:
            os.makedirs('checkpoints', exist_ok=True)
            checkpoint_path = f'checkpoints/model_epoch_{epoch+1}.pth'
            torch.save(model.state_dict(), checkpoint_path)
            print(f"Checkpoint saved: {checkpoint_path}")
    
    torch.save(model.state_dict(), 'models/final_transformer.pth')
    print(f"Final model saved: models/final_transformer.pth")
    
    print(f"\nTraining completed! Best validation loss: {best_val_loss:.4f}")
    
    return model

if __name__ == "__main__":
    trained_model = train_model()