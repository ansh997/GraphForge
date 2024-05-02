import json
import os
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from torch.quantization import quantize_dynamic

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print("Using device:", device)

custom_cache_dir = './'
api_token = os.getenv('HF_API_TOKEN')
if not api_token:
    raise ValueError("HF_API_TOKEN is unset")

tokenizer = AutoTokenizer.from_pretrained(
    "meta-llama/Llama-2-7b-chat-hf",
    token=api_token
)

model = AutoModelForCausalLM.from_pretrained(
    "meta-llama/Llama-2-7b-chat-hf",
    torch_dtype=torch.bfloat16,
    low_cpu_mem_usage=True,
    token=api_token
)

model.to(device)

#model = LlamaForCausalLM.from_pretrained("meta-llama/Llama-2-7b-hf", cache_dir=custom_cache_dir, token=api_token)
#tokenizer = LlamaTokenizer.from_pretrained("meta-llama/Llama-2-7b-hf", cache_dir=custom_cache_dir, token=api_token)
#odel = quantize_dynamic(model, {torch.nn.Linear}, dtype=torch.qint8).to(device)

def inject_prompt(question):
    with torch.no_grad():
        inputs = tokenizer(question, return_tensors="pt").to(device)
        outputs = model.generate(**inputs)
        response = tokenizer.decode(outputs[0], skip_special_tokens=True)
        return response

# Define data directories
question_folder = '../../data/curated_data/'
prediction_path = './output/'

# Process each file in the directory
for json_path in os.listdir(question_folder):
    json_file = open(question_folder + json_path, 'r')
    data = json.load(json_file)

    all_records = []
    output = prediction_path + json_path.split('.')[0] + '.json'

    print("Working on file", json_path)

    for item in data:
        id_ = item['id']
        algorithm = item['algorithm']
        text_encoding = item['text_encoding']
        question = item['question']
        answer = item['answer']

        print("Processing question no.:", id_, "of", len(data))

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

