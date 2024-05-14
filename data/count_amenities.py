import json
from collections import Counter

# Load JSON data from a file
def load_json(filename):
    with open(filename, 'r') as file:
        return json.load(file)

# Count amenities
def count_amenities(data):
    amenities = []
    for element in data:
        if 'amenities' in element:
            amenities.extend(element['amenities'])
    return Counter(amenities)

# Main function to load data, count amenities, and print counts
def main():
    input_filename = 'output.json'  # Name of the input JSON file
    
    # Load the data
    data = load_json(input_filename)
    
    # Count amenities and get a Counter object
    amenities_counts = count_amenities(data)
    
    # Sort the amenities by count in descending order and print/write them
    for amenity, count in amenities_counts.most_common():
        print(f"{amenity}: {count}")
    
    # Output the counts to a file in sorted order
    output_filename = 'amenities_counts.txt'  # Name of the output file
    with open(output_filename, 'w') as file:
        for amenity, count in amenities_counts.most_common():
            file.write(f"{amenity}: {count}\n")

if __name__ == '__main__':
    main()
