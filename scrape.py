from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.options import Options
import time
import undetected_chromedriver as uc
from fake_useragent import UserAgent
import re
import random
import json
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from concurrent.futures import ThreadPoolExecutor, as_completed
from selenium.common.exceptions import NoSuchElementException, TimeoutException, ElementNotInteractableException, MoveTargetOutOfBoundsException, StaleElementReferenceException
from selenium.webdriver.common.action_chains import ActionChains

code_list = []

# Get the list of codes from the txt file named 'codes.txt'
with open('codes.txt', 'r') as file:
    for line in file:
        code_list.append(line.strip())

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

def get_driver(url):
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
    driver.get(url)
    return driver

def remove_cookie(driver):
    try:
        # Locate the button using XPath and click it
        # Update the XPath as needed based on the button's position in the HTML structure
        button = driver.find_element(By.XPATH, "//div[@class='RxNS-button-content' and text()='Reject all']")
        button.click()
    except NoSuchElementException:
        print("Element not found")


def get_hotels(driver, max_attempts=3):
    attempts = 0
    while attempts < max_attempts:
        try:
            WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//*[contains(@class, 'hotel-name')]//a")))
            remove_cookie(driver)
            time.sleep(5)  # Allow time for dynamic content to load

            hotels = driver.find_elements(By.XPATH, "//*[contains(@class, 'hotel-name')]//a")
            for hotel in hotels:
                try:
                    name = hotel.text
                    url = hotel.get_attribute("href")
                    store_hotels(name, url, driver.current_url)
                except NoSuchElementException:
                    print("Failed to fetch hotel info, the element might have become stale or was not found.")
                    continue  # Skip this hotel and try the next one
            break  # Successfully processed all hotels, break out of the retry loop
        except (StaleElementReferenceException, TimeoutException) as e:
            attempts += 1
            print(f"Attempt {attempts}/{max_attempts} failed due to {type(e).__name__}. Retrying...")
            time.sleep(2)  # Wait before retrying

    if attempts == max_attempts:
        print(f"Max attempts reached for URL: {driver.current_url}. Logging URL and taking a screenshot.")
        log_failed_attempt(driver)

def log_failed_attempt(driver):
    with open('failed_urls.txt', 'a') as file:
        file.write(driver.current_url + '\n')
    screenshot_name = 'failed_page_' + driver.current_url.split('/')[-1] + '.png'
    driver.get_screenshot_as_file(screenshot_name)

def get_next_page(driver, page_number):
    try:
        # Wait for the next page button to be clickable
        next_page = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, f"//button[@aria-label='Page {page_number + 1}']")))
        
        # Scroll to the element in a human-like randomized manner with slow scroll
        actions = ActionChains(driver)
        actions.move_to_element(next_page).perform()
        time.sleep(random.uniform(0.5, 1.5))

        # Click the next page button
        next_page.click()
        return True  # Successfully clicked the next page
    except (TimeoutException, WebDriverException) as e:
        print(f"Attempt to find next page button failed: {e}")
        return False  # Failed to find/click the next page button


# Store in a json file with name and url
def store_hotels(name, url, current_url):
    print(f"Storing {name} and {url}")

    # Get country, state and city from current url
    city, state, country = parseUrl(current_url)
    json_data = {
        "name": name,
        "url": url,
        "city": city,
        "state": state,
        "country": country
    }

    # Initialize data list
    data = []

    # If file does not exist, create it with an empty list
    if not os.path.exists('hotels.json'):
        with open('hotels.json', 'w') as file:
            json.dump([], file)
    else:
        # If file exists, load existing data
        with open('hotels.json', 'r') as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError:
                print("File is empty or corrupt, starting fresh...")
                data = []

    # Check to see if name is already in the data
    for item in data:
        if item["name"] == name:
            print("Name already exists, skipping...")
            return

    # Append new hotel to data list
    data.append(json_data)

    # Write updated data back to file
    with open('hotels.json', 'w') as file:
        json.dump(data, file, indent=4)

def parseUrl(url):
    # Updated regular expression to optionally match city, state, and correctly capture country
    pattern = re.compile(r"hotel-search/(?:([^,]+?),)?(?:([^,]+?),)?([^,]+?)-p\d+/")

    match = pattern.search(url)

    if match:
        city = match.group(1) or "Unknown"
        state = match.group(2)
        country = match.group(3)
    else:
        city, state, country = "Unknown", None, "Unknown"

    return city, state, country

if __name__ == "__main__":
    for code in code_list:
        url = f"https://www.momondo.com/hotel-search/{code}/2024-08-10/2024-08-12/1adults?sort=rank_a&fs=property-type=-rental:apartment,rental:cabin,rental:condo,rental:cottage,rental:homestay,rental:holhome,rental:villa"
        driver = get_driver(url)

        # Initialize a counter for failed attempts to find the next page
        failed_attempts = 0

        # Get the hotels
        for i in range(1, pages_to_scrape + 1):
            get_hotels(driver)
            success = get_next_page(driver, i)
            if not success:
                failed_attempts += 1
                if failed_attempts >= 2:
                    print("Failed to find next page button twice, moving to the next code.")
                    break  # Exit the loop for the current code and move to the next one
            else:
                failed_attempts = 0  # Reset counter on successful navigation
            time.sleep(5)

        print('Done with the current code, quitting the driver in 5 seconds...')
        time.sleep(5)
        driver.quit()
