import json
import os

# Assuming you are running this in an environment where 'question_folder' is correctly defined
question_folder = './output/'
outputs_folder = "./results/"

def safe_parse_prediction(prediction):
    # Safely parse the prediction string to handle lists formatted as strings and remove unwanted characters
    if isinstance(prediction, str):
        # Strip brackets and split by commas, then strip spaces from each element
        cleaned_prediction = prediction.replace("[", "").replace("]", "").replace("'", "").strip()
        return set(x.strip() for x in cleaned_prediction.split(",") if x.strip())
    elif isinstance(prediction, list):
        # If the prediction is already a list, handle normally
        return set(prediction)
    else:
        return set()

def calculate_accuracy(data):
    accuracies = []
    for entry in data:
        # Normalize and split the answer, and clean the prediction
        answer_set = set(entry['answer'].replace('.', '').split(', '))
        prediction_set = safe_parse_prediction(entry['prediction'])

        # Calculate accuracy by intersection over union method
        if len(answer_set) > 0:
            accuracy = len(answer_set.intersection(prediction_set)) / len(answer_set) * 100
        else:
            accuracy = 100.0 if not prediction_set else 0.0
        accuracies.append(accuracy)

    # Return average accuracy if data is not empty
    return sum(accuracies) / len(accuracies) if accuracies else 0

def calculate_exact_match_accuracy(data):
    matches = 0
    for entry in data:
        # Compare sets directly for exact matches
        answer_set = set(entry['answer'].replace('.', '').split(', '))
        prediction_set = safe_parse_prediction(entry['prediction'])
        if answer_set == prediction_set:
            matches += 1

    return 100 * matches / len(data) if data else 0

# Process all JSON files in the directory
results = {}
for json_path in os.listdir(question_folder):
    with open(os.path.join(question_folder, json_path), 'r') as json_file:
        data = json.load(json_file)

    average_accuracy = calculate_accuracy(data)
    exact_match_accuracy = calculate_exact_match_accuracy(data)
    results[json_path] = {
        'average_accuracy': average_accuracy,
        'exact_match_accuracy': exact_match_accuracy
    }
    print(f"{exact_match_accuracy:.2f}%")

# Save the results to a JSON file
os.makedirs(outputs_folder, exist_ok=True)
with open(os.path.join(outputs_folder, 'results.json'), 'w') as results_file:
    json.dump(results, results_file, indent=4)
    
    


