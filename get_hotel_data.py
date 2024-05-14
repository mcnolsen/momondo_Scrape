from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.options import Options
import time
import undetected_chromedriver as uc
from fake_useragent import UserAgent
import requests
import random
import json
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from concurrent.futures import ThreadPoolExecutor, as_completed
from selenium.common.exceptions import NoSuchElementException, TimeoutException, ElementNotInteractableException, MoveTargetOutOfBoundsException, StaleElementReferenceException, ElementClickInterceptedException
from selenium.webdriver.common.action_chains import ActionChains

viewports = [
    # Laptops and Desktops
    (1280, 800),   # Some small laptop screens
    (1366, 768),   # Average Laptop screens
    (1440, 900),   # Older 19" monitors
    (1536, 864),   # Average desktop screens
    (1600, 900),   # Mid-range desktop screens
    (1920, 1080),  # HD desktop screens
    (2560, 1440),  # QHD screens
    (3840, 2160),  # 4K UHD screens
]
hotels_json = "hotels.json"
pages_to_scrape = 10

amenityList = []

def get_driver():
    options = Options()
    ua = UserAgent()
    userAgent = ua.random
    options.add_argument(f'user-agent={userAgent}')
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-features=VizDisplayCompositor")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-features=IsolateOrigins,site-per-process")
    
    # Get the current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Construct the full path to chromedriver
    chromedriver_path = os.path.join(current_dir, 'chromedriver.exe')

    driver = uc.Chrome(use_subprocess=True, driver_executable_path=chromedriver_path, options=options)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    return driver

def remove_cookie(driver):
    time.sleep(2)
    try:
        # Locate the button using XPath and click it
        # Update the XPath as needed based on the button's position in the HTML structure
        button = driver.find_element(By.XPATH, "//div[@class='RxNS-button-content' and text()='Reject all']")
        actions = ActionChains(driver)
        actions.move_to_element(button).perform()
        button.click()
    except NoSuchElementException:
        print("Cookie element not found")
    except ElementClickInterceptedException:
        driver.execute_script("arguments[0].click();", button)

        # After handling the overlay, re-locate the button and try clicking again
    try:
        # Wait for the button to be clickable again after overlay is dismissed
        button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@class='RxNS-button-content' and text()='Reject all']"))
        )
        button.click()
    except TimeoutException:
        print("Cookie button not clickable after handling overlay.")
    except StaleElementReferenceException:
        print("Element became stale after attempting to click.")
    except NoSuchElementException:
        print("Cookie element not found after overlay dismissed.")


def get_hotel_urls():
    # Initialize data list
    data = []

    # Load hotels from hotels.json
    if os.path.exists('hotels.json'):
        with open('hotels.json', 'r') as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError:
                print("hotels.json is empty or corrupt, starting fresh...")
                data = []

    # Initialize list for already scraped hotels
    scraped_hotels = []

    # Load hotels from hotels-data.json
    if os.path.exists('hotels-data.json'):
        with open('hotels-data.json', 'r') as file:
            try:
                scraped_hotels = json.load(file)
            except json.JSONDecodeError:
                print("hotels-data.json is empty or corrupt, no data to compare.")

    # Filter hotels that have not been scraped
    filtered_data = []
    scraped_urls = {hotel['url'] for hotel in scraped_hotels}  # Create a set of URLs for faster lookup
    for hotel in data:
        if hotel['url'] not in scraped_urls:
            filtered_data.append(hotel)

    return filtered_data


def close_icon(driver):
    try:
        close_icon_el = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'close') and contains(@aria-label, 'Close')]")))
        time.sleep(random.uniform(0.4, 1))

        close_icon_el.click()
        
    except NoSuchElementException:
        print("Close icon element not found")
    except TimeoutException:
        print('Timed out trying to find close icon button')

def update_hotels_json(new_hotel_data):

    # Add to new file 
    try:
        with open('hotels-data.json', 'r+') as file:
            # Read the current data
            try:
                data = json.load(file)
            except json.JSONDecodeError:
                data = []
            
            # Append the new hotel data
            data.append(new_hotel_data)
            
            # Move the file pointer to the beginning of the file to overwrite it
            file.seek(0)
            
            # Write the updated data
            json.dump(data, file, indent=4)
            
            # Truncate the file to the new size
            file.truncate()
            
    except FileNotFoundError:
        print("hotels-data.json file not found, creating a new one.")
        with open('hotels-data.json', 'w') as file:
            json.dump([new_hotel_data], file, indent=4)
            
    except Exception as e:
        print(f"An error occurred while updating the hotels.json file: {e}")

def get_hotel_data(driver, hotel):
    driver.get(hotel['url'])

    remove_cookie(driver)
    close_icon(driver)

    address_el = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//*[contains(@class, 'address')]")))
    address = address_el.text

    try: 
        star_el = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'stars-in-title')]//span")))
        stars = star_el.text[0]
    except TimeoutException:
        stars = "No stars found"

    rating = None
    review_count = None
    # Get the rating. Can be displayed in different ways, so we need to check for all possibilities
    try:
        rating_el = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'rating-score-wrapper')]//span[contains(@class, 'rating-score')]")))
        # Need to use get_attribute to get the textContent, as .text does not work
        rating = rating_el.get_attribute("textContent")
        if rating:
            # Get review count
            review_count_el = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'review-summary-wrapper')]//div[contains(@class, 'review-count')]")))
            review_count = review_count_el.get_attribute("textContent")
    except TimeoutException:
        try:
            if not rating:
                rating_el = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//button[contains(@class, 'rating-card')]//span[contains(@class, 'rating-score')]")))
                rating = rating_el.text

            if rating:
                # Get review count
                review_count_el = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'rating-score-wrapper')]//div[contains(@class, 'review-count')]")))
                review_count = review_count_el.get_attribute("textContent")
        except TimeoutException:
            if not rating:
                rating = "No rating found"
            if not review_count:
                review_count = "No review count found"

    # Can be displayed in different ways, so we need to check for all possibilities
    try:
        read_more_button = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, "//div[text()='Read more']")))
        actions = ActionChains(driver)
        actions.move_to_element(read_more_button).perform()
        time.sleep(random.uniform(0.3,1.2))
        read_more_button.click()
    except TimeoutException:
        try: 
            read_more_button = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, "//button[text()='Read more']")))
            actions = ActionChains(driver)
            actions.move_to_element(read_more_button).perform()
            time.sleep(random.uniform(0.3,1.2))
            read_more_button.click()
        except TimeoutException:
            # Then there is no read more button. We can just get the text
            read_more_button = None
    
    # Allow time for the description to expand
    time.sleep(random.uniform(0.5, 1.2))

    try:
        desc_el = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'desc-wrap--full')]")))
        desc = desc_el.text
    except TimeoutException:
        desc = "No description found"

    # Scroll to, then click the button starting with the text "Show all" to expand the amenities list
    try:
        show_all_button = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'Show all')]")))
        actions = ActionChains(driver)
        actions.move_to_element(show_all_button).perform()
        time.sleep(random.uniform(0.3,1.2))
        show_all_button.click()
    except TimeoutException:
        print("No 'Show all' button found")

    # Allow time for the amenities list to expand
    time.sleep(random.uniform(0.5, 1.2))

    # Get all amenities. Find all div elements that contains the class 'amenity-category', get the ul and then all the text of the li elements
    amenities = driver.find_elements(By.XPATH, "//div[contains(@class, 'amenity-category')]//ul//li")
    amenityData = []
    for amenity in amenities:
        amenityData.append(amenity.text)

        # Count unique amenities from all hotels
    for amenity in amenityData:
        if amenity not in amenityList:
            amenityList.append(amenity)

    hotelData = {'name': hotel['name'], 'url': hotel['url'], 'country': hotel['country'], 'state': hotel['state'], 'city': hotel['city'], 'address': address, 'rating': rating, 'review_count': review_count, 'stars': stars, 'description': desc, 'amenities': amenityData }

    update_hotels_json(hotelData)
    print(hotelData)
    return hotelData

if __name__ == "__main__":
    driver = get_driver()

    data = get_hotel_urls()

    for hotel in data:
        print(f"Getting data for {hotel['url']}")
        get_hotel_data(driver, hotel)
    print(amenityList)
    print('Done, quitting the driver in 5 seconds...')
    time.sleep(5)
    driver.quit()


    amenityUnique = ['', 'Electric kettle', 'Special diet menus (on request)', 'Restaurant', 'Bar/Lounge', 'Food can be delivered to guest accommodation', 'Coffee shop', 'Minibar', 'Microwave', 'Breakfast in the room', 'Tea/coffee maker', 'Kettle', 'Refrigerator', 'Coffee machine', 'ATM on-site', 'Business center', 'Car rental', 'Wake-up service', 'Concierge service', 'Currency exchange on-site', 'Mini-market on site', 'Meeting/Banquet facilities', 'Room service', 'Key card access', 'Express check-out', '24hr front desk', 'Conference rooms', 'Kitchen', 'Terrace/Patio', 'Air-conditioned', 'Washing machine', 'Tumble dryer', 'Linens', 'Towels', 'Flat-screen TV', 'TV', 'Free Wi-Fi', 'Wi-Fi available in all areas', 'Internet', 'Fan', 'Fire extinguisher', 'Free toiletries', 'Shampoo', 'Smoke alarms', 'No smoking', 'Pets allowed on request. Charges may apply.', 'Upper floors accessible by stairs', 'Private entrance', 'Iron and ironing board', 'Contactless check-in/check-out', 'First-aid kit', 'Window', 'Kitchenware', 'Stovetop', 'Ice maker', 'Toaster', 'Dishwasher', 'Oven', 'Hairdryer', 'Toilet', 'Shower', 'Parking', 'Wardrobe or closet', 'Spa and wellness center', 'Outdoor pool', 'Fitness center', 'Free parking', 'Daily housekeeping', 'Face masks for guests available', 'Physical distancing in dining areas', 'Physical distancing rules', 'Property is cleaned by professional cleaning companies', 'Process in place to check health of guests', 'Hand sanitizer in guest accommodation and key areas', 'Screens or physical barriers placed between staff and guests in appropriate areas', 'Use of cleaning chemicals that are effective against coronavirus', 'Guest accommodation is disinfected between stays', 'All plates, cutlery, glasses and other tableware have been sanitized', 'Safe', 'Delivered food is securely covered', 'Guests can opt-out of accommodation cleaning', 'Staff follow all safety protocols as directed by local authorities', 'Heating', 'Private bathroom', 'Seating area', 'Telephone', 'Carpeted', 'Alarm clock', 'Sofa bed', 'Desk', 'Safety deposit box', 'Entire unit wheelchair accessible', 'Increased accessibility', 'Elevator', 'Adapted bath', 'Pets not allowed', 'Radio', 'Shared lounge/TV area', 'Cable or satellite TV', 'Pay-per-view channels', 'Laundry facilities', 'Laundry service', 'Private parking', 'Babysitting or child care', 'Cribs available', 'Adults only', 'Body soap', 'Trash cans', 'Conditioner', 'Bathtub', 'Toilet paper', 'CCTV in common areas', 'CCTV outside property', 'Carbon monoxide detector', '24-hour security', 'Air purifiers', 'Bottle of water', 'Feather pillow', 'Clothes rack', 'Entire unit located on ground floor', 'Accessible by elevator', 'Upper floors accessible by elevator', 'Shared kitchen', 'Kitchenette', 'Slippers', 'Soundproof rooms', 'City view', 'Storage available', 'Game room', 'Pool table', 'Clothes dryer', 'Blender', 'Dishes', 'Dining area', 'Video library', 'Books', 'DVD player', 'Foosball table', 'Games for adults', 'Deadbolt locks', 'Living room', 'Soap and Shampoo Provided', 'Central heating', 'Kids toys', 'Kid-friendly', 'Baby safety gates', 'Games for kids', "Children's high chair", 'Outdoor furniture', 'Garden', 'Garage', 'Dining room', 'Valet parking', 'Guest accommodation sealed after cleaning', 'EV charging station', 'Hot tub', 'Bathrobe', 'Balcony', 'Pool', 'Grill', 'Housekeeping', 'Fireplace', 'Golf', 'Walk-in shower', 'Dining table', 'Fax/photocopying', 'Key access', 'Non-smoking rooms available', 'Roll-in shower', 'Shower chair', 'Toilet with grab rails', 'Designated smoking area', 'Family rooms', 'Sea view', 'Sofa', 'Electric blankets', 'Beach access', 'Wine glasses', 'Indoor pool', 'Lockers', 'Beauty salon', 'Toothbrush', 'Spa', 'Kids meals']