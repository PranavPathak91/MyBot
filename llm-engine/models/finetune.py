from typing import List, Dict, Any
import torch
from torch.utils.data import Dataset, DataLoader

class PersonalStyleDataset(Dataset):
    def __init__(self, texts: List[str], labels: List[str]):
        self.texts = texts
        self.labels = labels

    def __len__(self):
        return len(self.texts)

    def __getitem__(self, idx):
        return {"text": self.texts[idx], "label": self.labels[idx]}

class StyleFineTuner:
    def __init__(self, model, tokenizer, device="cuda" if torch.cuda.is_available() else "cpu"):
        """Initialize the fine-tuning manager."""
        self.model = model
        self.tokenizer = tokenizer
        self.device = device
        self.model.to(device)

    def prepare_dataset(self, texts: List[str], labels: List[str]) -> DataLoader:
        """Prepare dataset for fine-tuning."""
        dataset = PersonalStyleDataset(texts, labels)
        return DataLoader(dataset, batch_size=4, shuffle=True)

    def train(self, train_loader: DataLoader, epochs: int = 3):
        """Fine-tune the model."""
        optimizer = torch.optim.AdamW(self.model.parameters(), lr=5e-5)
        
        for epoch in range(epochs):
            self.model.train()
            total_loss = 0
            
            for batch in train_loader:
                optimizer.zero_grad()
                
                inputs = self.tokenizer(
                    batch["text"],
                    padding=True,
                    truncation=True,
                    return_tensors="pt"
                ).to(self.device)
                
                outputs = self.model(**inputs, labels=inputs["input_ids"])
                loss = outputs.loss
                
                loss.backward()
                optimizer.step()
                
                total_loss += loss.item()
            
            avg_loss = total_loss / len(train_loader)
            print(f"Epoch {epoch+1}/{epochs}, Average Loss: {avg_loss:.4f}")

    def save_model(self, path: str):
        """Save the fine-tuned model."""
        self.model.save_pretrained(path)
        self.tokenizer.save_pretrained(path)
