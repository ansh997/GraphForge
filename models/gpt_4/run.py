import json
import os
from openai import OpenAI
from config import Config

client = OpenAI(api_key=Config.openai_key)

def inject_prompt(question):

    # Append user's prompt to the conversation, with or without an image
    messages_to_send = [{
        "role": "user",
        "content": question  + "\n\n Just provide me the answer. your output should not contain any conversation"
    }]
    


    # API Call
    response = client.chat.completions.create(
        model="gpt-4-turbo-2024-04-09",
        messages=messages_to_send,
        max_tokens=100,
    )

    return response


question_folder = '/home/pranav/GraphForge/data/curated_data/'
prediction_path = './output_test/'

for json_path in os.listdir(question_folder):
	
	json_file = open(question_folder + json_path, 'r')
	data = json.load(json_file)

	all_records = []
	output = prediction_path + json_path.split('.')[0]

	print("Working on file", json_path)

	for item in data:
		id_ = item['id']
		algorithm = item['algorithm']
		text_encoding = item['text_encoding']
		question = item['question']
		answer = item['answer']

		print("Passing question no. : ", id_, "/", len(data))

		prediction = inject_prompt(question)
		prediction = prediction.choices[0].message.content

		data_to_append = {
			'id': id_, 
			'algorithm': algorithm,
			'text_encoding':text_encoding,
			'question': question,
			'answer': answer,
			'prediction':prediction,
			}
		
		all_records.append(data_to_append)
		with open(output, 'w') as f:
			json.dump(all_records, f, indent=4)
	

		





