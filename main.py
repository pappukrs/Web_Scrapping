from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pymongo
import time

def scrape_bse_website():
    # Setup Chrome WebDriver
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run Chrome in headless mode
    chrome_driver_path = r"C:\Users\HP\OneDrive\Desktop\chromedriver-win64\chromedriver.exe"  # Adjust the path accordingly
    service = Service(executable_path=chrome_driver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # Open BSE India website
    driver.get("https://www.bseindia.com")

    # Wait for the page to fully load
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

    # Extract the page source
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')

    # Find all elements containing h1 and p tags
    h1_elements = soup.find_all("h1")
    p_elements = soup.find_all("p")

    # Extract text from h1 and p elements
    h1_texts = [element.text.strip() for element in h1_elements]
    p_texts = [element.text.strip() for element in p_elements]

    # Combine h1 and p texts
    combined_data = [{"h1": h1_text, "p": p_text} for h1_text, p_text in zip(h1_texts, p_texts)]

    return combined_data

def save_to_mongodb(data):
    client = pymongo.MongoClient("mongodb+srv://pappu:pappu123@cluster0.whsucgh.mongodb.net/")
    db = client["bse_data"]
    collection = db["homepage_data"]
    if data:  # Check if data is not empty
        collection.insert_many(data)
        print("Data saved to MongoDB")
    else:
        print("No data to save")

def main():
    scraped_data = scrape_bse_website()  # Scrape BSE website homepage
    save_to_mongodb(scraped_data)  # Save homepage data to MongoDB

if __name__ == "__main__":
    main()
