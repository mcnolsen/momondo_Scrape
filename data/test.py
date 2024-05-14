import json

# Specify the path to the JSON file
file_path = 'hotels-data_updated.json'

# Load the JSON file
with open(file_path) as file:
    data = json.load(file)

# Count the number of objects
num_objects = len(data)

# Print the result
print(f"The number of objects in the JSON file is: {num_objects}")