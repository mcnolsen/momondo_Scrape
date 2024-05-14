import json
import googlemaps
import sys
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
# Function to load hotel data from a JSON file
def load_hotel_data(filename):
    try:
        with open(filename, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

# Function to save hotel data to a JSON file
def save_hotel_data(data, filename):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)

# Function to get latitude and longitude for an address
def get_lat_lon(address, gmaps):
    try:
        geocode_result = gmaps.geocode(address)
        if geocode_result:
            latitude = geocode_result[0]['geometry']['location']['lat']
            longitude = geocode_result[0]['geometry']['location']['lng']
            return latitude, longitude
        else:
            return None, None
    except Exception as e:
        print(f"Error occurred during geocoding: {e}")
        return None, None

# Main function to update hotel data with latitude and longitude
def main():
    api_key = GOOGLE_API_KEY 
    updated_filename = 'hotels_data_cleaned.json'  # Updated data filename
    try:
        # Initialize the Google Maps client
        gmaps = googlemaps.Client(key=api_key)
        
        # Load the updated hotel data if it exists
        hotels = load_hotel_data(updated_filename)
        total_hotels = len(hotels)
        processed_count = 0

        # Iterate over each hotel and update with latitude and longitude if needed
        for hotel in hotels:
            # Only process if latitude and longitude are missing
            if 'latitude' not in hotel or 'longitude' not in hotel:
                if 'address' in hotel and hotel['address']:
                    latitude, longitude = get_lat_lon(hotel['address'], gmaps)
                    if latitude is not None and longitude is not None:
                        hotel['latitude'] = latitude
                        hotel['longitude'] = longitude
            processed_count += 1
            sys.stdout.write(f"\rProcessed {processed_count} out of {total_hotels} hotels.")
            sys.stdout.flush()
        
        # Save the updated hotel data
        save_hotel_data(hotels, updated_filename)
        print("\nHotel data has been updated with latitude and longitude.")

    except Exception as e:
        print(f"\nAn error occurred: {e}. Attempting to save progress...")
        save_hotel_data(hotels, updated_filename)

if __name__ == '__main__':
    main()
