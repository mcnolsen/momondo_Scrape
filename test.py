import json
# Load and list the last 5 hotels stored in the json file
with open('hotels.json', 'r') as file:
    data = json.load(file)

    for hotel in data[-5:]:
        print(hotel)

