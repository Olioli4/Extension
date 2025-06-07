# example.py
# Simple script to prompt for a URL, fetch the content, and print the raw HTTP response or parsed content.

import requests
import re

def parse_netflix_url(url):
    """
    Fetch the given URL and return the image URL if found, else None.
    """
    try:
        response = requests.get(url, headers={'User-Agent': 'Python Example Script'})
        text = response.text
        # Write the raw response to requests.txt for debugging
        try:
            with open("requests.txt", "w", encoding="utf-8") as f:
                f.write(text)
        except Exception as file_err:
            print(f"Error writing requests.txt: {file_err}")
        
        search_text = text
        image_value = None
        image_match = re.search(r'<img alt="" src=(["\'])(.*?)\1', search_text)
        if image_match:
            image_value = image_match.group(2)
        if image_value:
            return image_value
        # Fallback to JSON if present
        try:
            data = response.json()
            image_value = data.get('image') if isinstance(data, dict) else None
            if image_value:
                return image_value
        except Exception:
            pass
        return None
    except Exception as e:
        print("Error fetching URL:", e)
        return None

if __name__ == "__main__":
    # For manual testing only: main.py provides the URL in production
    url = input("Enter a URL to fetch: ")
    image = parse_netflix_url(url)
    print("Image:", image)