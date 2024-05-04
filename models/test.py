import json
import os
import torch
import random
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline


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
    token=api_token, 
    cache_dir=custom_cache_dir
)
tokenizer = AutoTokenizer.from_pretrained(
    "microsoft/Phi-3-mini-128k-instruct", 
    token=api_token,
    cache_dir=custom_cache_dir
)


model.to(device)


pipe = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
)

generation_args = {
    "max_new_tokens": 200,
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
    return output[0]['generated_text']

print(inject_prompt("How are you today?"))
print(inject_prompt("How are you today?"))
print(inject_prompt("How are you today?"))
print(inject_prompt("How are you today?"))
print(inject_prompt("How are you today?"))