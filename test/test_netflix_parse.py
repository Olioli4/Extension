# test_netflix_parse.py
"""
Test for the parse_netflix_url function in netflix_parse.py
"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from netflix_parse import parse_netflix_url

def test_parse_netflix_url():
    # Example Netflix title URL (public, non-authenticated page)
    url = "https://www.netflix.com/watch/81630670?trackId=14170035"  # Example: Stranger Things
    titel, image_url = parse_netflix_url(url)
    print(f"Parsed titel: {titel}")
    print(f"Parsed image_url: {image_url}")
    assert titel is not None and len(titel) > 0, "Title should not be empty"
    assert image_url is not None and image_url.startswith("http"), "Image URL should be valid"

if __name__ == "__main__":
    test_parse_netflix_url()
    print("Test completed.")
