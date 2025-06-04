# example.py
# Simple script to prompt for a URL, fetch the content, and print the raw HTTP response or parsed content.

import requests
import re

if __name__ == "__main__":
    url = input("Enter a URL to fetch: ")
    try:
        response = requests.get(url, headers={'User-Agent': 'Python Example Script'})
        print("Status:", response.status_code)
        print("Headers:", dict(response.headers))
        print("\n--- Content (truncated to 1000 chars) ---\n")
        print(response.text[:1000])

        # Find the first line containing '"name"' and extract the next string value
        lines = response.text.split('\n')
        name_value = None
        image_value = None
        
        for line in lines:
            if name_value is None and '"name"' in line:
                match = re.search(r'"name"\s*:\s*"([^"\r\n]+)"', line)
                if match:
                    name_value = match.group(1)
            
            if image_value is None and '"image"' in line:
                match = re.search(r'"image"\s*:\s*"([^"\r\n]+)"', line)
                if match:
                    image_value = match.group(1)
            
            if name_value is not None and image_value is not None:
                break
        
        # Print extracted values
        if name_value or image_value:
            print("\n--- Extracted Values ---")
            if name_value:
                print(f"Name: {name_value}")
            if image_value:
                print(f"Image: {image_value}")
        else:
            print("\n--- No name or image values found ---")
            
    except Exception as e:
        print("Error fetching URL:", e)
