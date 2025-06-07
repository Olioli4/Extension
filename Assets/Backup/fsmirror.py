# fsmirror.py
# Extracts DVD poster image and title from FSMirror page URL

import requests
import re
import sys

def parse_fsmirror_url(url):
    """
    Fetch the FSMirror page and extract the DVD poster image URL and title.
    Returns (title, image_url) or (None, None) on failure.
    """
    try:
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        html = response.text
        # Try to extract the title (from <title> or a specific element if needed)
        title_match = re.search(r'<title>(.*?)</title>', html, re.IGNORECASE | re.DOTALL)
        title = title_match.group(1).strip() if title_match else ''
        # Try to extract the DVD poster image from the dvd-container
        img_match = re.search(r'<div class="dvd-container"[^>]*onclick="showDvdPoster\(\)"[^>]*>.*?<img[^>]*src=["\']([^"\']+)["\']', html, re.DOTALL)
        image_url = img_match.group(1) if img_match else None
        # Fallback: try to extract from background-image CSS
        if not image_url:
            bg_match = re.search(r'background-image:\s*url\(["\']([^"\']+)["\']\)', html)
            image_url = bg_match.group(1) if bg_match else None
        return title, image_url
    except Exception as e:
        print(f"Error parsing FSMirror URL: {e}")
        return None, None

if __name__ == "__main__":
    if len(sys.argv) > 1:
        url = sys.argv[1]
    else:
        url = input("Enter FSMirror URL: ")
    title, image_url = parse_fsmirror_url(url)
    print(f"Title: {title}\nImage URL: {image_url}")
