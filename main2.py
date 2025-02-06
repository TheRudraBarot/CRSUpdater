from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

# Set up headless Chrome
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

service = Service("/root/updater/chromedriver-linux64/chromedriver")  # Adjust path if necessary
driver = webdriver.Chrome(service=service, options=chrome_options)

URL = "https://www.canada.ca/en/immigration-refugees-citizenship/services/immigrate-canada/express-entry/rounds-invitations.html"
# Load page
driver.get(URL)

# Wait for JavaScript to load
driver.implicitly_wait(10)

# Extract content
try:
    content_element = driver.find_element(By.XPATH, "/html/body/main/div[1]/section/ul[2]")
    content_text = content_element.text.strip()
    print("Extracted content:", content_text)
except Exception as e:
    print("Failed to find element:", e)

driver.quit()
