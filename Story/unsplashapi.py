import requests
import json
import random
from PIL import Image

def download_image_from_api(keyword):
    """Downloads a random image from the Unsplash API based on the given keyword."""
    
    # Enter your Unsplash API access key here
    access_key = "jOcdgbjZX5ic3TbyQBHW4AcVqIsJFDUr1OYNynXnP_Q"

    # Construct the API request URL with the given keyword
    api_url = f"https://api.unsplash.com/search/photos?query={keyword}&client_id={access_key}"

    # Send a GET request to the API endpoint
    response = requests.get(api_url)

    # Convert the response to JSON format
    result = json.loads(response.text)

    # Extract the list of image results from the JSON response
    images = result["results"]

    # Choose a random image from the list of results
    chosen_image = random.choice(images)

    # Extract the URL of the chosen image
    image_url = chosen_image["urls"]["regular"]

    # Download the image data from the URL
    image_data = requests.get(image_url).content

    # Return the image data as a binary file object
    return image_data

def display_image_from_file(file_path):
    """Displays the image file at the given path using the Pillow library."""
    
    # Open the image file using the Pillow library
    image = Image.open(file_path)

    # Display the image using the default image viewer on your system
    image.show()

# Example usage:
# Download an image related to "mountains"
image_data = download_image_from_api("mountains")

# Save the image data to a file
with open("mountain_image.jpg", "wb") as f:
    f.write(image_data)

# Display the downloaded image using the Pillow library
display_image_from_file("mountain_image.jpg")
