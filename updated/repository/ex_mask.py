

# Example sentences to test
sentences = [
    "राम [MASK] बाज़ार जा रहा है।",
    "सीता [MASK] किताब पढ़ती है।"
]

# Process sentences
results = process_multiple_sentences(sentences)
for res in results:
    print(res)



# from transformers import AutoModelForMaskedLM, AutoTokenizer
# import torch
# import time

# # Load the base masked language model
# # model = AutoModelForMaskedLM.from_pretrained("ai4bharat/IndicBERTv2-MLM-only")
# model =AutoModelForMaskedLM.from_pretrained("updated/repository/IndicBERTv2-MLM-only")
# # Load the tokenizer
# tokenizer = AutoTokenizer.from_pretrained("updated/repository/IndicBERTv2-MLM-only")

# # Function to generate output using the Masked Language Model
# def gen_op(sentence):
#     model.eval()
#     inputs = tokenizer(sentence, return_tensors="pt")
#     # print(inputs)
#     with torch.no_grad():
#         outputs = model(**inputs)
#         # print(outputs,'opp')
#         logits = outputs.logits
#         masked_index = (inputs['input_ids'] == tokenizer.mask_token_id).nonzero(as_tuple=True)[1]
#         # print(logits.shape)
#         # print(masked_index)
#         predicted_tokens = logits[0, masked_index].argmax(dim=-1)
#         # print(predicted_tokens)
#         predicted_words = tokenizer.decode(predicted_tokens)
#         # print(predicted_words)
#         return predicted_words

# # Function to substitute the masked tokens with predictions
# def gen_sen(sentence, op_tokens):
#     sent_list = sentence.strip().split()
#     # print(sent_list,'sl')
#     count = 0
#     op_tok_list = op_tokens.split()
#     for word_inx in range(len(sent_list)):
#         if sent_list[word_inx] == "[MASK]":
#             sent_list[word_inx] = op_tok_list[count]
#             count += 1
#     return " ".join(sent_list)

# # Function to handle vibhakti prediction based on masks
# def gen_vibhakti_prediction(sentence):
#     if "<>" in sentence:
#         op = gen_op(sentence.strip())
#         # print(op,'opp')
#         op = gen_sen(sentence, op)
#         return op
#     else:
#         return sentence

# Main execution
# if __name__ == "__main__":
#     print(gen_vibhakti_prediction("इस पाठ [MASK] आप दैनिक जीवन [MASK] भूगोल के महत्व [MASK] [MASK] [MASK] सीख सकेंगे "))
    # 15वीं सदी में ईसा का जन्म हुआ था।
    # इस पाठ से आप दैनिक जीवन में भूगोल के महत्व को बारे से सीख सकेंगे
    # इस पाठ से आप दैनिक जीवन में भूगोल के महत्व के बारे में सीख सकेंगे
    # print(f"Time taken to process {len(sentences)} sentences: {time_taken:.4f} seconds")

    # with open("verified") as vm:
    #     vm_input = vm.read().strip().split()
    #     gen_vibhakti_prediction(vm_input)
    #     print(vm_input)
    #     for text in vm_input:
    #         if text == "[MASK]":
    #             print(text)
    #             gen_vibhakti_prediction(text)
# ==========================================================
# from transformers import AutoTokenizer, AutoModelForMaskedLM
# import torch

# # Load the tokenizer and model
# tokenizer = AutoTokenizer.from_pretrained("ai4bharat/IndicBERTv2-MLM-only")
# model = AutoModelForMaskedLM.from_pretrained("ai4bharat/IndicBERTv2-MLM-only")

# # Input sentence with multiple masks
# sentence = "उसने राम [MASK] कार्यालय [MASK] [MASK] आधारशिला [MASK] रखी"

# # Tokenize the input
# input_ids = tokenizer(sentence, return_tensors="pt").input_ids

# # Predict the masked tokens
# with torch.no_grad():
#     outputs = model(input_ids)

# # Get the indices of the [MASK] tokens
# masked_indices = (input_ids == tokenizer.mask_token_id).nonzero(as_tuple=True)[1]
# logits = outputs.logits[0, masked_indices]

# # Convert predictions to tokens
# predicted_ids = torch.argmax(logits, dim=-1)
# predicted_tokens = tokenizer.convert_ids_to_tokens(predicted_ids)

# # Replace the [MASK] tokens with the predicted tokens
# input_ids[0, masked_indices] = predicted_ids

# # Decode the updated input_ids back into a sentence
# predicted_sentence = tokenizer.decode(input_ids[0], skip_special_tokens=True)

# # Print the sentence with the [MASK] replaced by the predicted tokens
# print(predicted_sentence)
# =====================================================================
from transformers import AutoModelForMaskedLM, AutoTokenizer
from peft import LoraConfig, get_peft_model
import torch
import time
import re
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
            sent_list[word_inx] = op_tok_list[count]
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

# Main execution
# if __name__ == "__main__":
#     sentences = [
#         "इस पाठ [MASK] आप दैनिक जीवन [MASK] भूगोल के महत्व के बारे [MASK] सीख सकेंगे ।",
#         "पृथ्वी की सतह [MASK] लगातार परिवर्तन हो रहा है ।",
#         "पूर्व की भांति आज भी किसी क्षेत्र का भौगोलिक विवरण रिपोर्ट, यात्रा डायरियों और गजेटियरों [MASK] उपलब्ध है ।",
#         "वर्तमान [MASK] मानचित्र की रचना भौगोलिक सूचना तंत्र जी.आई.एस. के उपकरणों द्वारा उपग्रह छायाचित्रों के प्रयोग से किया जा सकता है।",
#         "सीता [MASK] कल [MASK] बाज़ार [MASK] गई थी",
#         "तथा उस क्षेत्र [MASK] होने वाली स्थानिक प्रक्रियाओं के विषय [MASK] निष्कर्ष निकालते है ।",
#         "इन सभी की प्राप्ति संसाधनों के सतत रूप [MASK] प्रयोग द्वारा ही की जा सकती है ।",
#         "इतिहास के विभिन्न कालों [MASK] भूगोल के विभिन्न रूपों [MASK] परिभाषित किया गया है ।",
#         "मैंने [MASK] चाय [MASK] दो [MASK] बार पी",
#         "राम अयोध्या [MASK] रहते थे",
#         "राम 6 बजे उठता है",
#         "राम राजनीति [MASK] चर्चा करता है"
#     ]
    
#     results, time_taken = process_multiple_sentences(sentences)
    
#     for sentence, result in zip(sentences, results):
#         print(f"Input: {sentence}\nOutput: {result}\n")
    
#     print(f"Time taken to process {len(sentences)} sentences: {time_taken:.4f} seconds")
