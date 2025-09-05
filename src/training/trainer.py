import torch
import torch.nn as nn
import torch.optim as optim
from tqdm import tqdm

class TransformerTrainer:
    def __init__(self, model, tokenizer, device, learning_rate=0.0001):
        self.model = model
        self.tokenizer = tokenizer
        self.device = device
        
        self.optimizer = optim.Adam(
            model.parameters(),
            lr=learning_rate,
            weight_decay=0.001
        )
        
        self.scheduler = optim.lr_scheduler.StepLR(self.optimizer, step_size=5, gamma=0.8)
        self.criterion = nn.CrossEntropyLoss(ignore_index=tokenizer.tokenizer.pad_token_id)
    
    def train_epoch(self, train_loader, epoch_num):
        self.model.train()
        epoch_loss = 0
        
        progress_bar = tqdm(train_loader, desc=f'Epoch {epoch_num}')
        for batch in progress_bar:
            src_ids = batch['src_ids'].to(self.device)
            tgt_ids = batch['tgt_ids'].to(self.device)
            
            self.optimizer.zero_grad()
            output = self.model(src_ids, tgt_ids[:, :-1])
            
            loss = self.criterion(
                output.contiguous().view(-1, output.size(-1)),
                tgt_ids[:, 1:].contiguous().view(-1)
            )
            
            loss.backward()
            torch.nn.utils.clip_grad_norm_(self.model.parameters(), 1.0)
            self.optimizer.step()
            
            epoch_loss += loss.item()
            progress_bar.set_postfix({'loss': f'{loss.item():.4f}'})
        
        return epoch_loss / len(train_loader)
    
    def validate(self, val_loader):
        self.model.eval()
        total_loss = 0
        
        with torch.no_grad():
            for batch in val_loader:
                src_ids = batch['src_ids'].to(self.device)
                tgt_ids = batch['tgt_ids'].to(self.device)
                
                output = self.model(src_ids, tgt_ids[:, :-1])
                loss = self.criterion(
                    output.contiguous().view(-1, output.size(-1)),
                    tgt_ids[:, 1:].contiguous().view(-1)
                )
                total_loss += loss.item()
        
        return total_loss / len(val_loader)
    
    def step_scheduler(self):
        self.scheduler.step()