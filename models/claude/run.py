import json
import os
import random
import anthropic
import time 

random.seed(42)

client = anthropic.Anthropic(
    api_key="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"
)


def inject_prompt(question):
    message = client.messages.create(
        model="claude-3-haiku-20240307",
        max_tokens=1024,
        messages=[
            {"role": "user", 
             "content": question + "\n\n Just provide me the answer. your output should not contain any conversation"}
        ]
    )
    return message.content[0].text
    

# Define data directories
question_folder = '../../data/curated_data/'
prediction_path = './output/'

if not os.path.exists(prediction_path):
    os.makedirs(prediction_path)

# Process each file in the directory
i = 0
for json_path in os.listdir(question_folder):
    i += 1
    if i <= 53:
        continue
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

    i = 0
    for item in sampled_data:
        id_ = item['id']
        algorithm = item['algorithm']
        text_encoding = item['text_encoding']
        question = item['question']
        answer = item['answer']

        print("Processing question no.:", id_, "of", len(sampled_data))

        prediction = inject_prompt(question)
        # sleep for 1.5 seconds
        time.sleep(1.5)

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
        print(output)

    print("Finished processing file", json_path)


