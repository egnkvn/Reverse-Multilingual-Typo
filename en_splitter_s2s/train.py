import json
from transformers import T5Tokenizer, T5ForConditionalGeneration, get_linear_schedule_with_warmup
from torch.utils.data import Dataset, DataLoader
import torch
import torch.nn as nn
import torch.optim as optim
from tqdm import tqdm 
def load_data(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
    return data

def get_residual_text(input_text, gt_text):
    residual_text = input_text.replace(gt_text, "").strip()
    return residual_text

class TextDataset(Dataset):
    def __init__(self, data, tokenizer, max_length=512):
        self.data = data
        self.tokenizer = tokenizer
        self.max_length = max_length

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        sample = self.data[idx]
        
        input_text = sample["input"]
        gt_text = sample["gt"]
        
        residual_text = get_residual_text(input_text, gt_text)
        
        target_text = f"{gt_text} [SEP] {residual_text}" if residual_text else gt_text
        
        input_encoding = self.tokenizer(
            input_text, padding="max_length", truncation=True, max_length=self.max_length, return_tensors="pt"
        )
        target_encoding = self.tokenizer(
            target_text, padding="max_length", truncation=True, max_length=self.max_length, return_tensors="pt"
        )

        input_ids = input_encoding["input_ids"].squeeze(0)
        attention_mask = input_encoding["attention_mask"].squeeze(0)
        labels = target_encoding["input_ids"].squeeze(0)
        
        labels[labels == self.tokenizer.pad_token_id] = -100

        return {
            "input_ids": input_ids,
            "attention_mask": attention_mask,
            "labels": labels,
        }

tokenizer = T5Tokenizer.from_pretrained("t5-base")
model = T5ForConditionalGeneration.from_pretrained("t5-base")
device = torch.device("cuda:6" if torch.cuda.is_available() else "cpu")
model = model.to(device)

train_data = load_data("/data2/jerome/tech_write_split_data/train.json")
val_data = load_data("/data2/jerome/tech_write_split_data/valid.json")
train_dataset = TextDataset(train_data, tokenizer)
val_dataset = TextDataset(val_data, tokenizer)

# DataLoader
bz = 12
train_loader = DataLoader(train_dataset, batch_size=bz, shuffle=True)
val_loader = DataLoader(val_dataset, batch_size=bz, shuffle=False)

scaler = torch.cuda.amp.GradScaler()
optimizer = optim.AdamW(model.parameters(), lr=5e-5)
num_epochs = 5
eval_steps = 5000
total_steps = len(train_loader) * num_epochs

scheduler = get_linear_schedule_with_warmup(
    optimizer,
    num_warmup_steps=0,
    num_training_steps=total_steps
)

best_val_loss = float("inf")  
save_directory = "trained_t5_model" 

for epoch in range(num_epochs):
    model.train()
    total_loss = 0
    step = 0 
    progress_bar = tqdm(train_loader, desc=f"Epoch {epoch+1}/{num_epochs}")
    
    for batch in progress_bar:
        input_ids = batch["input_ids"].to(device)
        attention_mask = batch["attention_mask"].to(device)
        labels = batch["labels"].to(device)

        optimizer.zero_grad()
        
        with torch.cuda.amp.autocast(dtype=torch.bfloat16):
            outputs = model(
                input_ids=input_ids,
                attention_mask=attention_mask,
                labels=labels
            )
            loss = outputs.loss
        
        scaler.scale(loss).backward()
        scaler.step(optimizer)
        scaler.update()
        scheduler.step()

        total_loss += loss.item()
        progress_bar.set_postfix({"Loss": total_loss / (progress_bar.n + 1)})
        
        if (step + 1) % eval_steps == 0:
            model.eval()
            total_val_loss = 0
            with torch.no_grad():
                for val_batch in tqdm(val_loader, desc="Evaluation..."):
                    input_ids = val_batch["input_ids"].to(device)
                    attention_mask = val_batch["attention_mask"].to(device)
                    labels = val_batch["labels"].to(device)

                    with torch.cuda.amp.autocast(dtype=torch.bfloat16):
                        outputs = model(
                            input_ids=input_ids,
                            attention_mask=attention_mask,
                            labels=labels
                        )
                        loss = outputs.loss

                    total_val_loss += loss.item()

            avg_val_loss = total_val_loss / len(val_loader)
            print(f"Step {step + 1} - Val Loss: {avg_val_loss:.4f}")

            if avg_val_loss < best_val_loss:
                best_val_loss = avg_val_loss
                print(f"Best validation loss improved to {best_val_loss:.4f}. Saving model...")
                model.save_pretrained(f"{save_directory}/{step+1}")
                tokenizer.save_pretrained(f"{save_directory}/{step+1}")
            model.train()

        step += 1   

    avg_train_loss = total_loss / len(train_loader)
    print(f"Epoch {epoch + 1} - Train Loss: {avg_train_loss:.4f}")