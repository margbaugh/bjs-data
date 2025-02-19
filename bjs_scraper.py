import requests
from bs4 import BeautifulSoup

# URL of the page to scrape
url = "https://bjs.ojp.gov/data-collection/mortality-correctional-institutions-mci-formerly-deaths-custody-reporting-program#2-0"

# Send a GET request to fetch the raw HTML content
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    print("Successfully retrieved the webpage.")
else:
    print("Failed to retrieve the webpage.")
    exit()

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(response.text, 'html.parser')

# Extract text or data from specific tags or sections of the page
# Extract all <a> tags, which define hyperlinks
links = soup.find_all('a')

# Loop through the found links and print the href attribute (the actual URL)
for link in links:
    href = link.get('href')
    if href:  # Only print the link if href attribute exists
        print(href)

