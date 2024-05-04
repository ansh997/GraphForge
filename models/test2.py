import json
import os
import torch
import random
from transformers import AutoModelForCausalLM, AutoTokenizer

random.seed(42)
torch.random.manual_seed(0)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print("Using device:", device)

custom_cache_dir = '/scratch/ananth.muppidi/TIDL'

api_token = os.getenv('HF_API_TOKEN')
if not api_token:
    raise ValueError("HF_API_TOKEN is unset")

model = AutoModelForCausalLM.from_pretrained(
    "microsoft/Phi-3-mini-128k-instruct", 
    device_map="cuda", 
    torch_dtype="auto", 
    trust_remote_code=True, 
    token=api_token
)
tokenizer = AutoTokenizer.from_pretrained(
    "microsoft/Phi-3-mini-128k-instruct", 
    token=api_token
)


model.to(device)


pipe = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
)

generation_args = {
    "max_new_tokens": 500,
    "return_full_text": False,
    "temperature": 0.0,
    "do_sample": False,
}

def inject_prompt(question):
    messages = [
        {"role": "user", 
         "content": question + " \n\n Please respond with only the answer, and nothing else. Try to be as consise as possible."
        }
    ]
    output = pipe(messages, **generation_args)
    return output[0]

question_folder = '/scratch/ananth.muppidi/TIDL/data/curated_data/'
prediction_path = './output/'

if not os.path.exists(prediction_path):
    os.makedirs(prediction_path)

# Process each file in the directory
for json_path in os.listdir(question_folder):
    json_file = open(question_folder + json_path, 'r')
    data = json.load(json_file)
    
    class_dict = {}
    
    for entry in data:
        class_name = entry['algorithm']
        if class_name not in class_dict:
            class_dict[class_name] = []
        class_dict[class_name].append(entry)
        
    # Step 4: Randomly sample 100 dictionaries from each class
    sampled_data = []
    for class_name, entries in class_dict.items():
        sampled_entries = random.sample(entries, min(10, len(entries)))
        sampled_data.extend(sampled_entries)
    

    all_records = []
    output = prediction_path + json_path.split('.')[0] + '.json'

    print("Working on file", json_path)

    for item in sampled_data:
        id_ = item['id']
        algorithm = item['algorithm']
        text_encoding = item['text_encoding']
        question = item['question']
        answer = item['answer']

        print("Processing question no.:", id_, "of", len(sampled_data))

        prediction = inject_prompt(question)

        data_to_append = {
            'id': id_,
            'algorithm': algorithm,
            'text_encoding': text_encoding,
            'question': question,
            'answer': answer,
            'prediction': prediction,
        }

        all_records.append(data_to_append)

    with open(output, 'w') as f:
        json.dump(all_records, f, indent=4)

    print("Finished processing file", json_path)

