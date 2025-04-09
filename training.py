from transformers import DistilBertForQuestionAnswering, DistilBertTokenizerFast
from transformers import Trainer, TrainingArguments, default_data_collator
from datasets import load_dataset
import torch

# Step 1: Load your JSONL dataset
dataset = load_dataset('json', data_files="questions1.jsonl")
print("Dataset structure:", dataset)

# Step 2: Load pre-trained DistilBERT tokenizer and model for QA
model_name = 'twmkn9/distilbert-base-uncased-squad2'
tokenizer = DistilBertTokenizerFast.from_pretrained(model_name)
model = DistilBertForQuestionAnswering.from_pretrained(model_name)

# Step 3: Define preprocessing function
def preprocess_function(examples):
    # Tokenize questions and contexts
    tokenized = tokenizer(
        examples['question'],
        examples['context'],
        truncation=True,
        padding='max_length',
        max_length=512,
        return_offsets_mapping=True
    )
    
    # Initialize arrays for start/end positions
    start_positions = []
    end_positions = []
    
    # Process each example
    for i, offset in enumerate(tokenized.offset_mapping):
        # Get answer
        answer_dict = examples['answers'][i]
        answer_text = answer_dict['text'][0]  # First answer text
        start_char = answer_dict['answer_start'][0]  # First answer position
        end_char = start_char + len(answer_text)
        
        # Convert character positions to token positions
        sequence_ids = tokenized.sequence_ids(i)
        
        # Find start position in tokens
        start_position = 0
        for idx, (token_start, token_end) in enumerate(offset):
            # Skip special tokens (like [CLS], [SEP], etc.)
            if sequence_ids[idx] is None:
                continue
                
            # Only consider tokens that are part of the context (sequence_id = 1)
            if sequence_ids[idx] != 1:
                continue
                
            if token_start <= start_char < token_end:
                start_position = idx
                break
        
        # Find end position in tokens
        end_position = 0
        for idx, (token_start, token_end) in enumerate(offset):
            # Skip special tokens
            if sequence_ids[idx] is None:
                continue
                
            # Only consider context tokens
            if sequence_ids[idx] != 1:
                continue
                
            if token_start <= end_char <= token_end:
                end_position = idx
                break
        
        # Add to lists
        start_positions.append(start_position)
        end_positions.append(end_position)
    
    # Remove offset mapping as it's not needed for training
    tokenized.pop("offset_mapping")
    
    # Add start and end positions
    tokenized["start_positions"] = start_positions
    tokenized["end_positions"] = end_positions
    
    return tokenized

# Apply preprocessing
tokenized_datasets = dataset.map(
    preprocess_function, 
    batched=True, 
    remove_columns=dataset["train"].column_names
)

print("Tokenized dataset features:", tokenized_datasets["train"].features)

# Step 4: Convert datasets to PyTorch tensors
def convert_to_tensors(examples):
    # Convert all values to tensors
    result = {}
    for key, value in examples.items():
        if key in ["start_positions", "end_positions"]:
            result[key] = torch.tensor(value, dtype=torch.long)
        else:
            result[key] = torch.tensor(value)
    return result

# Apply tensor conversion
tensor_datasets = tokenized_datasets.map(
    convert_to_tensors,
    batched=False  # Process one example at a time
)

# Step 5: Split into train and validation sets
train_dataset = tensor_datasets["train"].train_test_split(test_size=0.1)["train"]
val_dataset = tensor_datasets["train"].train_test_split(test_size=0.1)["test"]

# Step 6: Define training arguments
training_args = TrainingArguments(
    output_dir='./results',
    eval_strategy="epoch",
    learning_rate=3e-5,
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,
    num_train_epochs=3,
    weight_decay=0.01,
    logging_dir='./logs'
)

# Step 7: Initialize trainer with default data collator
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=val_dataset,
    data_collator=default_data_collator
)

# Step 8: Train the model
trainer.train()

# Step 9: Save the model
model.save_pretrained('./fine_tuned_model')
tokenizer.save_pretrained('./fine_tuned_model')
print("Training complete and model saved.")