from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import pymongo
from dotenv import load_dotenv
import os
load_dotenv()

DB_ATLAS = os.getenv("DB_ATLAS")
CHROME_DRIVER_PATH = os.getenv("CHROME_DRIVER_PATH")

def scrape_bse_website(CHROME_DRIVER_PATH):
    # Setup Chrome WebDriver
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run Chrome in headless mode
    #chrome_driver_path = r"C:\Users\HP\OneDrive\Desktop\chromedriver-win64\chromedriver.exe"  # Adjust the path accordingly
    service = Service(executable_path=CHROME_DRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # Open BSE India website
    driver.get("https://www.bseindia.com/")

    # Wait for the page to fully load
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

    # Extract h1 headings
    h1_elements = driver.find_elements(By.TAG_NAME, "h1")
    h1_texts = [element.text.strip() for element in h1_elements]

    # Extract PDF links
    pdf_links = []
    pdf_elements = driver.find_elements(By.XPATH, "//a[contains(@href, '.pdf')]")
    for element in pdf_elements:
        pdf_links.append((element.text.strip(), element.get_attribute("href")))

    # Extract XBRL codes
    xbrl_elements = driver.find_elements(By.CSS_SELECTOR, "div.xbrl-code")
    xbrl_codes = [element.text.strip() for element in xbrl_elements]

    # Combine all data
    combined_data = {"headings": h1_texts, "pdf_links": pdf_links, "xbrl_codes": xbrl_codes}

    return combined_data

def save_to_mongodb(data):
    client = pymongo.MongoClient("mongodb+srv://pappu:pappu123@cluster0.whsucgh.mongodb.net/")
    db = client["bse_data"]
    collection = db["homepage_data"]
    collection.insert_one(data)
    print("Data saved to MongoDB")

def main():
    scraped_data = scrape_bse_website(CHROME_DRIVER_PATH)  # Scrape BSE website homepage
    save_to_mongodb(scraped_data)  # Save homepage data to MongoDB

if __name__ == "__main__":
    main()
