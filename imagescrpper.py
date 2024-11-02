import requests
from bs4 import BeautifulSoup
import os

# URL of the website you want to scrape
url = 'https://www.google.com/search?sca_esv=b81127c47418f4ee&rlz=1C1FHFK_enIN1097IN1097&q=nike+shoes&udm=2&fbs=AEQNm0Aa4sjWe7Rqy32pFwRj0UkWxyMMuf0D-HOMEpzq2zertRy7G-dme1ONMLTCBvZzSlhEjTPx-bvxK8WZAYFqhMlnssUYBEjg0UYvmIqirHAW81O7EXYEqtwsK5NVSHFg83FK51jmoIleT4VgMX-AjYh_-EC4_8DBYT7qlEw_USGmQdt3wzh5WrKoxedJLu0AkqAaK9y8QfpGrc2uez22Yy8k7Rv5Yg&sa=X&sqi=2&ved=2ahUKEwibivKIvb2JAxX7TWwGHRqxJb8QtKgLegQIExAB&biw=1536&bih=695&dpr=1.25'  # Replace with the actual URL

# Create a directory to save logos
os.makedirs('logos', exist_ok=True)

# Send a GET request to the website
response = requests.get(url)

# Check if the request was successful
if response.status_code != 200:
    print("Failed to retrieve the webpage")
    exit()

soup = BeautifulSoup(response.text, 'html.parser')

# Find all image tags
images = soup.find_all('img')

downloaded_count = 0  # Counter for downloaded images

for img in images:
    # Get the image source
    img_url = img['src']
    
    # Check if the image URL ends with .png
    if img_url.endswith('.png'):
        if img_url.startswith('/'):  # Handle relative URLs
            img_url = url + img_url

        try:
            img_data = requests.get(img_url).content
            
            # Define the path to save the image
            img_name = os.path.join('logos', f'logo_{downloaded_count + 1}.png')
            
            # Write the image data to a file
            with open(img_name, 'wb') as handler:
                handler.write(img_data)
                
            downloaded_count += 1
            print(f'Downloaded: {img_name}')
        
        except Exception as e:
            print(f'Could not download {img_url}: {e}')

        # Stop if we've downloaded 50 images
        if downloaded_count >= 50:
            break

print(f'Total logos downloaded: {downloaded_count}')
