import csv
import requests
from bs4 import BeautifulSoup

base_url = "https://bjs.ojp.gov"

# Loop through the found links and print the href attribute (the actual URL)
# Add all of the subpages and file urls to a list
subpages = []
files = set()
metadata = []
for page in range(0,85):
    # URL of the page to scrape
    url = f"https://bjs.ojp.gov/library?page={page}#publications-pub-list-simple-filter-date-ehvbm-rwdqb5b2lk"
    # Send a GET request to fetch the raw HTML content
    response = requests.get(url, page)
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
    for link in links:
        href = link.get('href')
        if href:  # Only print the link if href attribute exists
            if "list?series_filter" in href or "library/publications/list" in href:
                continue # skip the ones that are just lists of pubs
            if "/library/publications/" in href:
                subpages.append(base_url+href)
                response = requests.get(base_url+href)
                temp_soup = BeautifulSoup(response.text, 'html.parser')
                # Extract all <a> tags, which define hyperlinks
                links = temp_soup.find_all('a')

                # Define a list of file extensions to look for
                file_extensions = ['.pdf', '.xls', '.xlsx', '.docx', '.csv', '.txt', '.zip']

                # Loop through the found links and check if the href contains any of the file extensions
                for link in links:
                    file_href = link.get('href')
                    if file_href:  # Only consider links with an href attribute
                        # Check if the href ends with a file extension from the list
                        if any(file_href.endswith(ext) for ext in file_extensions):
                            entry = {}
                            files.add(base_url+file_href)
                            entry["file"] = base_url+file_href
                            entry["page_found"]= base_url+href
                            metadata.append(entry)
print(subpages)
print(files)
print(metadata)
with open("metadata.csv", 'w') as f:
    writer = csv.DictWriter(f, fieldnames=["file", "page_found"])
    writer.writeheader()
    writer.writerows(metadata)
