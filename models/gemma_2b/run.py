import json
import os
import torch
import random
from transformers import AutoModelForCausalLM, AutoTokenizer
# from torch.quantization import quantize_dynamic
# device = "cpu"

random.seed(42)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print("Using device:", device)

custom_cache_dir = '/scratch/ananth.muppidi/TIDL'

api_token = os.getenv('HF_API_TOKEN')
if not api_token:
    raise ValueError("HF_API_TOKEN is unset")

tokenizer = AutoTokenizer.from_pretrained(
    "google/gemma-2b-it",
    token=api_token
)

model = AutoModelForCausalLM.from_pretrained(
    "google/gemma-2b-it",
    torch_dtype=torch.bfloat16,
    low_cpu_mem_usage=True,
    token=api_token,
    device_map='auto'
)

model.to(device)

def inject_prompt(question):
    with torch.no_grad():
        inputs = tokenizer(question+"\n\n Just provide me the answer. your output should not contain any conversation. Give me just one word answer wherever necessary and nothing else.",
        return_tensors="pt").to(device)
        outputs = model.generate(**inputs, max_length=10000)
        response = tokenizer.decode(outputs[0], skip_special_tokens=True)
        return response

# Define data directories
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

