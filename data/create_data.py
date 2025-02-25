import tensorflow as tf
import json
import os
tf.compat.v1.enable_eager_execution()

path = './tasks/'

directory_path = './curated_data'

# Create the directory if it does not exist
if not os.path.exists(directory_path):
    os.makedirs(directory_path)
    print(f"Directory '{directory_path}' was created.")
else:
    print(f"Directory '{directory_path}' already exists.")


for file_name in os.listdir(path):

  # Path to the TFRecord file
  file_path = path + file_name
  output = './curated_data/' + file_name.split('.')[0] + '.json'
  all_records = []

  # Feature description dictionary for parsing the TFRecord
  feature_description = {
      'algorithm': tf.io.FixedLenFeature([], tf.string),
      'question': tf.io.FixedLenFeature([], tf.string),
      'answer': tf.io.FixedLenFeature([], tf.string),
      'text_encoding': tf.io.FixedLenFeature([], tf.string),
      'id': tf.io.FixedLenFeature([], tf.string),
  }

  def _parse_function(example_proto):
      # Parse the input tf.train.Example proto using the dictionary above.
      return tf.io.parse_single_example(example_proto, feature_description)

  # Create a dataset from the TFRecord file
  dataset = tf.data.TFRecordDataset(file_path)
  parsed_dataset = dataset.map(_parse_function)


  # Iterate through the parsed dataset and add to list
  for parsed_record in parsed_dataset:
      record = {
          'id': parsed_record['id'].numpy().decode('utf-8'),
          'algorithm': parsed_record['algorithm'].numpy().decode('utf-8'),
          'text_encoding': parsed_record['text_encoding'].numpy().decode('utf-8'),
          'question': parsed_record['question'].numpy().decode('utf-8'),
          'answer': parsed_record['answer'].numpy().decode('utf-8'),
          
      }
      all_records.append(record)

  # Save the records to a JSON file
  with open(output, 'w') as f:
      json.dump(all_records, f, indent=4)

  print("Data has been saved to", output)

