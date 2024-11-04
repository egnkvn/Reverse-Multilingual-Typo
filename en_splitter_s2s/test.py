import json
from transformers import T5Tokenizer, T5ForConditionalGeneration
from torch.utils.data import Dataset, DataLoader
import torch
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
        
        input_ids = input_encoding["input_ids"].squeeze(0)
        attention_mask = input_encoding["attention_mask"].squeeze(0)

        return {
            "input_ids": input_ids,
            "attention_mask": attention_mask,
            "original_text": input_text,
            "target_text": target_text 
        }

device = torch.device("cuda:5" if torch.cuda.is_available() else "cpu")
model_directory = "trained_t5_model/75000" 
tokenizer = T5Tokenizer.from_pretrained(model_directory)
model = T5ForConditionalGeneration.from_pretrained(model_directory).to(device)

test_data = load_data("/data2/jerome/tech_write_split_data/test.json")
test_dataset = TextDataset(test_data, tokenizer)
test_loader = DataLoader(test_dataset, batch_size=16, shuffle=False)

def generate_text(input_ids, attention_mask):
    with torch.no_grad():
        outputs = model.generate(
            input_ids=input_ids,
            attention_mask=attention_mask,
            max_length=128, 
            num_beams=1,
            early_stopping=True
        )
    return [tokenizer.decode(output, skip_special_tokens=True) for output in outputs]

model.eval()
generated_texts = []
original_texts = []
target_texts = []

for batch in tqdm(test_loader, desc="Inference on test data"):

    input_ids = batch["input_ids"].to(device)
    attention_mask = batch["attention_mask"].to(device)
    original_texts.extend(batch["original_text"])
    target_texts.extend(batch["target_text"]) 

    generated_batch = generate_text(input_ids, attention_mask)
    generated_texts.extend(generated_batch)

output_file = "results.json"
with open(output_file, "w") as f:
    json.dump({"results": [{"original": orig, "target": tgt, "generated": gen} for orig, tgt, gen in zip(original_texts, target_texts, generated_texts)]}, f, indent=4)
print(f"Inference results saved to {output_file}")