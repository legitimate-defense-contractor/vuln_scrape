import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from PIL import Image
from io import BytesIO
import string

# Base URL of the website to crawl
base_url = "https://www.argeliuslabs.com"  # Change this to the website you'll host

def is_printable(s):
    """
    Check if all characters in a string are printable.
    """
    return all(c in string.printable for c in s)

def clean_metadata(metadata):
    """
    Clean metadata by removing non-printable characters from values.
    """
    cleaned_metadata = {}
    for key, value in metadata.items():
        if isinstance(value, bytes):
            # Attempt to decode bytes, and filter out non-printable characters
            try:
                decoded_value = value.decode('ascii', 'ignore')
                cleaned_value = ''.join(filter(is_printable, decoded_value))
            except UnicodeDecodeError:
                cleaned_value = '<binary data>'
        elif isinstance(value, str):
            cleaned_value = ''.join(filter(is_printable, value))
        else:
            cleaned_value = value  # Assume non-string, non-binary values are okay
        cleaned_metadata[key] = cleaned_value
    return cleaned_metadata


def download_images(url):
    """
    Downloads all images from a website and displays their metadata,
    excluding non-printable characters, in a human-readable format.
    """
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    images = soup.find_all('img')

    for img in images:
        img_url = urljoin(url, img.get('src'))
        print(f"\nDownloading image from: {img_url}")

        try:
            img_response = requests.get(img_url)
            img_name = img_url.split("/")[-1]

            # Save the image to the current directory
            with open(img_name, 'wb') as f:
                f.write(img_response.content)

            # Display image metadata
            with Image.open(BytesIO(img_response.content)) as img:
                metadata_for_print = clean_metadata(img.info)
                print(f"Metadata for '{img_name}':")
                for key, value in metadata_for_print.items():
                    print(f"  - {key}: {value}")
        except Exception as e:
            print(f"Error with image '{img_name}': {e}")

if __name__ == "__main__":
    base_url = "https://www.ratemypolarbear.com"  # Change to your target website
    download_images(base_url)
