import requests
from bs4 import BeautifulSoup
import os
import shutil

# Make a GET request to the webpage
url = "{{url_for('home')}}"  # Replace 'YOUR_URL_HERE' with the actual URL of the webpage
response = requests.get(url)

# Parse the HTML content
soup = BeautifulSoup(response.text, 'html.parser')

# Find all img tags within the gallery id
gallery_images = soup.find('div', id='gallery').find_all('img')

# Directory to save the images
output_directory = 'gallery_images'

# Create the directory if it doesn't exist
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# Download and save the images
for index, img in enumerate(gallery_images):
    img_url = img['src']
    img_name = f'image_{index + 1}.jpg'  # You can customize the naming convention here
    img_path = os.path.join(output_directory, img_name)

    # Download the image
    img_response = requests.get(img_url, stream=True)

    # Save the image to the output directory
    with open(img_path, 'wb') as out_file:
        shutil.copyfileobj(img_response.raw, out_file)
    del img_response

print('Images scraped successfully and saved to', output_directory)
