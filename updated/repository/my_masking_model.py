from transformers import AutoModelForMaskedLM, AutoTokenizer
from peft import LoraConfig, get_peft_model
import torch
import time
import re
import repository.constant
# from huggingface_hub import login
# token = "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"
# login(token=token, add_to_git_credential=True)
# Load the base masked language model
model = AutoModelForMaskedLM.from_pretrained("ai4bharat/IndicBERTv2-MLM-only")
# model = AutoModelForMaskedLM.from_pretrained("/home/varshith/Downloads/new_gen_example/updated/repository/hindi_fine_tuned_model1")
# Load the tokenizer
tokenizer = AutoTokenizer.from_pretrained("ai4bharat/IndicBERTv2-MLM-only")
# tokenizer = AutoModelForMaskedLM.from_pretrained("/home/varshith/Downloads/new_gen_example/updated/repository/IndicBERTv2-MLM-only")
# Define LoRA configuration
# lora_config = LoraConfig(
#     r=8,               # Low-rank matrix dimension
#     lora_alpha=16,     # Scaling factor for LoRA
#     target_modules=["query", "value"],  # Apply LoRA on attention layers (query, value)
#     lora_dropout=0.1,  # Dropout rate for LoRA layers
#     bias="none",       # No bias terms in LoRA layers
#     task_type="CAUSAL_LM"  # Task type
# )

# # Apply LoRA to the model
# model = get_peft_model(model, lora_config)
# Function to remove special characters but keep mask tokens intact
# Function to remove special characters but keep mask tokens intact
# def clean_sentence(sentence):
#     # Remove all special characters except [MASK] and words
#     return re.sub(r'[^a-zA-Z0-9[\]MASK\s]', '', sentence)

# Function to generate output using the Masked Language Model
def gen_op(sentence):
    # Clean the sentence before prediction (remove special characters)
    # cleaned_sentence = clean_sentence(sentence)
    
    # Clean the sentence before prediction (remove special characters)
    # cleaned_sentence = clean_sentence(sentence)
    model.eval()
    inputs = tokenizer(sentence, return_tensors="pt")
    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits
        masked_index = (inputs['input_ids'] == tokenizer.mask_token_id).nonzero(as_tuple=True)[1]
        predicted_tokens = logits[0, masked_index].argmax(dim=-1)
        predicted_words = tokenizer.decode(predicted_tokens)
        return predicted_words

# Function to substitute the masked tokens with predictions
def gen_sen(sentence, op_tokens):
    sent_list = sentence.strip().split()
    count = 0
    op_tok_list = op_tokens.split()
    for word_inx in range(len(sent_list)):
        if sent_list[word_inx] == "[MASK]":
            print(op_tok_list[count])
            if op_tok_list[count] in repository.constant.k7_postposition_list:
                sent_list[word_inx] = op_tok_list[count]
            else:
                sent_list[word_inx] = ''
            count += 1
    return " ".join(sent_list)

# Function to handle vibhakti prediction based on masks
def gen_vibhakti_prediction(sentence):
    if "[MASK]" in sentence:
        print(sentence,'sentttt')
        op = gen_op(sentence.strip())
        print(op,'opppp')
        op = gen_sen(sentence, op)
        return op
    else:
        print(sentence,'sentttt1')
        return sentence

# Function to process multiple sentences and measure execution time
def process_multiple_sentences(sentences):
    results = []
    
    start_time = time.time()
    
    for sentence in sentences:
        
        result = gen_vibhakti_prediction(sentence)
        # print(result,'resulttttttttt')
        results.append(result)
    # print(sentences,'senttttt')
    end_time = time.time()
    execution_time = end_time - start_time
    
    return results