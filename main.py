import requests
from lxml import html
import hashlib
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import datetime

# URL to monitor
URL = "https://www.canada.ca/en/immigration-refugees-citizenship/services/immigrate-canada/express-entry/rounds-invitations.html"

# XPath for the target content
XPATH = "/html/body/main/div[1]/section/ul[2]"

# File to store last hash
HASH_FILE = "./last_hash.txt"

# Email Configuration
SENDER_EMAIL = "therudrabarot@gmail.com"
RECEIVER_EMAIL = "therudrabarot@gmail.com"
SMTP_SERVER = "smtp-relay.gmail.com "
SMTP_PORT = 587
SMTP_USERNAME = SENDER_EMAIL
SMTP_PASSWORD = "Rudra@7832"

def fetch_content():
    """Fetches the webpage and extracts text content from the specified XPath."""
    response = requests.get(URL)
    tree = html.fromstring(response.content)
    
    # Extract content using XPath
    content_element = tree.xpath(XPATH)
    print(content_element)
    
    if content_element:
        content_text = content_element[0].text_content().strip()
        return content_text
    else:
        return None

def hash_content(content):
    """Creates a SHA256 hash of the content."""
    return hashlib.sha256(content.encode()).hexdigest()

def load_last_hash():
    """Loads the last saved hash."""
    if os.path.exists(HASH_FILE):
        with open(HASH_FILE, "r") as file:
            return file.read().strip()
    return None

def save_new_hash(new_hash):
    """Saves the new hash along with the current date."""
    with open(HASH_FILE, "w") as file:
        file.write(new_hash)

def send_email(update_text):
    """Sends an email with the updated content."""
    subject = "Express Entry CRS Score Update"
    body = f"The Express Entry details have changed:\n\n{update_text}\n\nCheck here: {URL}"

    msg = MIMEMultipart()
    msg["From"] = SENDER_EMAIL
    msg["To"] = RECEIVER_EMAIL
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())
        server.quit()
        print("Email sent successfully.")
    except Exception as e:
        print(f"Failed to send email: {e}")

def main():
    """Main function to check for updates and send notifications."""
    content = fetch_content()

    if not content:
        print("Failed to fetch content. Check the XPath.")
        return

    current_hash = hash_content(content)
    last_hash = load_last_hash()

    if current_hash != last_hash:
        print("Update detected! Sending email...")
        send_email(content)
        save_new_hash(current_hash)
    else:
        print("No updates found.")

if __name__ == "__main__":
    main()
