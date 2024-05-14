import json

import mysql.connector

import os
from dotenv import load_dotenv

# Load the environment variables
load_dotenv()

DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_DATABASE = os.getenv('DB_DATABASE')

# Connect to the MySQL database
db = mysql.connector.connect(
    user = DB_USER,
    password = DB_PASSWORD,
    host = DB_HOST,
    database = DB_DATABASE,
)

# Create a cursor object to execute SQL queries
cursor = db.cursor()

# Read the output.json file
with open('hotels_data_cleaned.json') as file:
    data = json.load(file)

# Translate country names to iso codes
def format_country(country_name):
    if country_name == 'United-States':
        return 'US'
    elif country_name == 'United-Kingdom':
        return 'GB'
    elif country_name == 'France':
        return 'FR'
    elif country_name == 'Germany':
        return 'DE'
    elif country_name == 'Italy':
        return 'IT'
    elif country_name == 'Spain':
        return 'ES'
    elif country_name == 'Denmark':
        return 'DK'
    elif country_name == 'Sweden':
        return 'SE'
    elif country_name == 'Norway':
        return 'NO'
    elif country_name == 'Finland':
        return 'FI'
    elif country_name == 'Faroe-Islands':
        return 'DK'
    elif country_name == 'Iceland':
        return 'IS'
    elif country_name == 'Ireland':
        return 'IE'
    elif country_name == 'Netherlands':
        return 'NL'
    elif country_name == 'Belgium':
        return 'BE'
    elif country_name == 'Switzerland':
        return 'CH'
    elif country_name == 'Turkiye':
        return 'TR'
    elif country_name == 'Greece':
        return 'GR'
    elif country_name == 'Portugal':
        return 'PT'
    elif country_name == 'Czech-Republic':
        return 'CZ'
    elif country_name == 'Poland':
        return 'PL'
    elif country_name == 'Monaco':
        return 'MC'
    elif country_name == 'Mexico':
        return 'MX'
    elif country_name == 'Austria':
        return 'AT'
    elif country_name == 'Australia':
        return 'AU'
    elif country_name == 'Thailand':
        return 'TH'
    elif country_name == 'Japan':
        return 'JP'
    elif country_name == 'Greenland':
        return 'DK'
    elif country_name == 'Malta':
        return 'MT'
    elif country_name == 'Hungary':
        return 'HU'
    elif country_name == 'Lithuania':
        return 'LT'
    elif country_name == 'Brazil':
        return 'BR'
    elif country_name == 'India':
        return 'IN'
    else:
        return country_name

# Iterate over the data and insert into the hotels table
for hotel in data:

    # Print the progress
    print(f"Inserting hotel: {hotel.get('name')}")

    # Extract the amenities for each hotel
    amenities = hotel.get('amenities', [])
    # Check if the amenities exist in the amenity list
    spa_amenities = ['spa', 'spa and wellness center','spa bath']
    fitness_center_amenities = ['fitness center', 'gym', 'fitness room']
    parking_amenities = ['free parking', 'parking (surcharge)', 'long-term parking (surcharge)', 'valet parking']
    wifi_amenities = ['free wi-fi', 'free internet', 'wi-fi (surcharge)', 'internet']
    pool_amenities = ['pool bar', 'pool with a view', 'indoor pool', 'outdoor pool', 'heated pool', 'infinity pool', 'rooftop pool', 'pool', 'private pool', 'saltwater pool', 'plunge pool', 'pool towels', 'pool table', 'pool cover', 'water slide']
    bar_amenities = ['pool bar', 'bar/lounge']
    cribs_amenities = ['cribs available']
    restaurant_amenities = ['restaurant', 'special diet menus (on request)', 'dining area', 'outdoor dining area', 'dining room', 'complimentary breakfast', 'continental breakfast', 'breakfast included']
    aircondition_amenities = ['air-conditioned', 'fan']
    airport_shuttle_amenities = ['airport shuttle', 'airport shuttle (surcharge)', 'free airport shuttle']
    washing_and_drier_amenities = ['washing machine', 'washer/dryer available in-room', 'tumble dryer']
    ev_charging_station_amenities = ['ev charging station']
    ocean_view_amenities = ['sea view']
    pet_friendly_amenities = ['pets not allowed', 'pets allowed on request. charges may apply.']
    casino_amenities = ['casino']
    kitchen_amenities = ['kitchen', 'kitchenette', 'kitchen/kitchenette', 'kitchenware']
    water_park_amenities = ['water park']
    beach_access_amenities = ['beachfront', 'beach access', 'private beach', 'beach chairs', 'beach towels']
    golf_amenities = ['golf']
    adults_only_amenities = ['adults only']
    kid_friendly_buffet_amenities = ['kid-friendly buffet']
    child_pool_amenities = ['child pool']
    playground_amenities = ['playground']
    increased_accessibility_amenities = ['increased accessibility']
    unit_wheelchair_accessible_amenities = ['entire unit wheelchair accessible']
    elevator_amenities = ['elevator']

    wifi = 'no'
    pool = 0

    if any(amenity in amenities for amenity in wifi_amenities):
        wifi = 'free'
    elif 'wi-fi (surcharge)' in amenities:
        wifi = 'surcharge'

    if any(amenity in amenities for amenity in pool_amenities):
        pool = 1

    bar = 1 if any(amenity in amenities for amenity in bar_amenities) else 0

    cribs = 1 if any(amenity in amenities for amenity in cribs_amenities) else 0

    restaurant = 1 if any(amenity in amenities for amenity in restaurant_amenities) else 0

    aircondition = 1 if any(amenity in amenities for amenity in aircondition_amenities) else 0

    # Check if the hotel has an airport shuttle. If it has, determine if it is free or paid
    airport_shuttle = 'no'
    if any(amenity in amenities for amenity in airport_shuttle_amenities):
        if 'free airport shuttle' in amenities:
            airport_shuttle = 'free'
        else:
            airport_shuttle = 'possible'
    
    washing_and_drier = 1 if any(amenity in amenities for amenity in washing_and_drier_amenities) else 0

    ev_charging_station = 1 if any(amenity in amenities for amenity in ev_charging_station_amenities) else 0

    ocean_view = 1 if any(amenity in amenities for amenity in ocean_view_amenities) else 0

    # Check if the hotel is pet-friendly. If it is, determine if there are charges
    pet_friendly = 'no pets'
    if any(amenity in amenities for amenity in pet_friendly_amenities):
        if 'pets allowed on request. charges may apply.' in amenities:
            pet_friendly = 'pets allowed on request'
        elif 'pets not allowed' in amenities:
            pet_friendly = 'no pets'

    casino = 1 if any(amenity in amenities for amenity in casino_amenities) else 0

    kitchen = 1 if any(amenity in amenities for amenity in kitchen_amenities) else 0

    water_park = 1 if any(amenity in amenities for amenity in water_park_amenities) else 0

    # Check if the hotel has beach access. If it has, determine if it is private beach or just beach access
    beach_access = 'no'
    if any(amenity in amenities for amenity in beach_access_amenities):
        if 'private beach' in amenities:
            beach_access = 'private beach'
        elif ['beachfront', 'beach access', 'beach chairs', 'beach towels'] in amenities:
            beach_access = 'beach access'
    
    golf = 1 if any(amenity in amenities for amenity in golf_amenities) else 0

    spa = 1 if any(amenity in amenities for amenity in spa_amenities) else 0

    fitness_center = 1 if any(amenity in amenities for amenity in fitness_center_amenities) else 0

    # Check if the hotel has parking. If it has, determine if it is free or paid
    parking = 'no'
    if any(amenity in amenities for amenity in parking_amenities):
        if 'free parking' in amenities or 'free valet parking':
            parking = 'free'
        elif 'parking (surcharge)' in amenities or 'long-term parking (surcharge)' in amenities or 'valet parking' in amenities:
            parking = 'surcharge'
    
    adults_only = 1 if any(amenity in amenities for amenity in adults_only_amenities) else 0

    kids_friendly_buffet = 1 if any(amenity in amenities for amenity in kid_friendly_buffet_amenities) else 0

    child_pool = 1 if any(amenity in amenities for amenity in child_pool_amenities) else 0

    playground = 1 if any(amenity in amenities for amenity in playground_amenities) else 0

    increased_accessibility = 1 if any(amenity in amenities for amenity in increased_accessibility_amenities) else 0

    unit_wheelchair_accessible = 1 if any(amenity in amenities for amenity in unit_wheelchair_accessible_amenities) else 0

    # Extract other hotel details
    country_name = hotel.get('country')
    hotel_url = hotel.get('url')
    name = hotel.get('name')
    state = hotel.get('state')
    city = hotel.get('city')
    address = hotel.get('address')
    rating = hotel.get('rating')
    review_count = hotel.get('review_count')
    stars = hotel.get('stars')
    description = hotel.get('description')
    lat = hotel.get('latitude')
    lon = hotel.get('longitude')

    # Format the country name to iso code
    country = format_country(country_name)

    # Insert the hotel details into the hotels table
    query = "INSERT INTO hotels (name, hotel_url, country, state, city, address, rating, review_count, stars, description, lat, lon, spa, fitness_center, pool, parking, wifi, bar, cribs, restaurant, aircondition, airport_shuttle, washing_and_drier, ev_charging_station, ocean_view, pet_friendly, casino, kitchen, water_park, beach_access, golf, adults_only, kids_friendly_buffet, child_pool, playground, increased_accessibility, unit_wheelchair_accessible) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    values = (name, hotel_url, country, state, city, address, rating, review_count, stars, description, lat, lon, spa, fitness_center, pool, parking, wifi, bar, cribs, restaurant, aircondition, airport_shuttle, washing_and_drier, ev_charging_station, ocean_view, pet_friendly, casino, kitchen, water_park, beach_access, golf, adults_only, kids_friendly_buffet, child_pool, playground, increased_accessibility, unit_wheelchair_accessible)
    cursor.execute(query, values)

# Commit the changes and close the database connection
db.commit()
db.close()