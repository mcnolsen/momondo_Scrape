import json

# Function to remove parentheses from a string
def remove_parentheses(s):
    return s.replace('(', '').replace(')', '')

# Function to convert each amenity to lowercase
def lowercase_amenities(amenities):
    return [amenity.lower() for amenity in amenities]

# Load JSON data from a file
def load_json(filename):
    with open(filename, 'r') as file:
        return json.load(file)

# Save JSON data to a file
def save_json(data, filename):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)

# Remove duplicates based on URL and return a list along with the count of duplicates removed
def remove_duplicates(data):
    unique_data = {}
    original_count = len(data)
    for element in data:
        if 'url' in element:
            unique_data[element['url']] = element
    unique_count = len(unique_data)
    duplicates_removed = original_count - unique_count
    return list(unique_data.values()), duplicates_removed

# Strip booking.com from the description if it exists
def strip_booking_description(description):
    return description.replace('Booking.com', '')

# Strip everything after the 'details' in the url. Keep the 'details' part
def strip_url_details(url):
    return url.split('details')[0] + 'details'

def remove_comma(s):
    return s.replace(',', '')

# Process JSON data
def process_data(data):
    # Remove duplicates first and get the count of duplicates removed
    processed_data, duplicates_removed = remove_duplicates(data)
    for element in processed_data:
        # Remove parentheses from review_count if it exists
        if 'review_count' in element:
            element['review_count'] = remove_parentheses(element['review_count'])
            # Remove commas from review_count if it exists
            element['review_count'] = remove_comma(element['review_count'])
        
        # Convert amenities to lowercase if they exist
        if 'amenities' in element:
            element['amenities'] = lowercase_amenities(element['amenities'])
        
        if 'description' in element:
            # Strip Booking.com from the description if it exists
            element['description'] = strip_booking_description(element['description'])
        
        if 'url' in element:
            # Strip everything after the 'details' in the url
            element['url'] = strip_url_details(element['url'])
            

    return processed_data, duplicates_removed

# Main function to load, process, and save JSON data
def main():
    input_filename = 'hotels-data_updated.json'  # Name of the input JSON file
    output_filename = 'hotels_data_cleaned.json'  # Name of the output JSON file
    
    # Load the data
    data = load_json(input_filename)
    
    # Process the data and get the count of duplicates removed
    processed_data, duplicates_removed = process_data(data)
    
    # Print the amount of duplicates removed
    print(f"Amount of duplicates removed: {duplicates_removed}")
    
    # Save the processed data
    save_json(processed_data, output_filename)

if __name__ == '__main__':
    main()
