# main.py
# Native messaging host and PyQt6 dialog for writing to ODS spreadsheet

from Functions import append_row_to_ods, read_native_message, send_native_message
from form_widget import inputbox
from netflix_parse import parse_netflix_url
from fsmirror import parse_fsmirror_url
import os
import datetime
import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer

# --- Config ---
ODS_PATH = "C:\\Users\\olivi\\Documents\\MeineAblage.ods"
SHEET_NAME = "Sheet1"

# --- Logging Control ---
ENABLE_DEBUG_LOG = True  # Set to False to disable debug logging

def log_debug(message):
    if ENABLE_DEBUG_LOG:
        with open("debug.log", "a", encoding="utf-8") as f:
            f.write(f"DEBUG: {message}\n")

# --- Main Execution ---
if __name__ == "__main__":
    log_debug("Script starting...")
    msg = read_native_message()
    log_debug(f"Received message: {msg}")
    if msg and msg.get('netflix') and msg.get('url'):
        url = msg['url']
        titel = msg.get('title', '')  # Get title from message sent by background.js
        log_debug(f"Calling parse_netflix_url with url: {url}")
        image_url = parse_netflix_url(url)
        log_debug(f"parse_netflix_url returned image_url={image_url}")
        episode = ""
        more = False
        seen_on = datetime.datetime.now().strftime('%d.%m.%Y')
        log_debug(f"Netflix: titel={titel}, image_url={image_url}, url={url}")
        image_for_form = image_url if image_url else "icon.png"
        titel, episode, more = inputbox(
            "Folgen",  # Dialog window title
            "Netflix-Eintrag",  # Static dialog title
            default_long_text=titel if titel else "",
            image_url=image_for_form
        )
        log_debug(f"Form result for Netflix: titel={titel}, episode={episode}, more={more}")
        append_row_to_ods(titel or '', episode, seen_on, url, more, image_for_form)
        log_debug("Successfully saved Netflix entry to ODS")
        send_native_message({"result": "OK"})
        log_debug("Response sent successfully")
        app = QApplication.instance()
        if app:
            app.quit()
        sys.exit(0)
    if msg and msg.get('fsmirror') and msg.get('url'):
        url = msg['url']
        log_debug(f"Calling parse_fsmirror_url with url: {url}")
        titel, image_url = parse_fsmirror_url(url)
        log_debug(f"parse_fsmirror_url returned titel={titel}, image_url={image_url}")
        episode = ""
        more = False
        seen_on = datetime.datetime.now().strftime('%d.%m.%Y')
        image_for_form = image_url if image_url else "icon.png"
        titel, episode, more = inputbox(
            "FSMirror",  # Dialog window title
            "FSMirror-Eintrag",  # Static dialog title
            default_long_text=titel if titel else "",
            image_url=image_for_form
        )
        log_debug(f"Form result for FSMirror: titel={titel}, episode={episode}, more={more}")
        append_row_to_ods(titel or '', episode, seen_on, url, more, image_for_form)
        log_debug("Successfully saved FSMirror entry to ODS")
        send_native_message({"result": "OK"})
        log_debug("Response sent successfully")
        app = QApplication.instance()
        if app:
            app.quit()
        sys.exit(0)
    if msg and 'text' in msg:
        titel = msg['text'] if msg['text'] else "Fill"
        url = msg.get('url', '')
        cover = msg.get('imageSrc', '')  # Extract the cover image source
        log_debug(f"Using titel from Chrome: {titel}")
        log_debug(f"Cover image source: {cover}")
    else:
        log_debug("No Chrome message, showing inputbox for first column")
        titel = "Fill"
        url = msg.get('url', '') if msg else ''
        cover = ""  # No cover for manual input
    log_debug("Showing inputbox for episode column")
    image_for_form = cover if cover else "icon.png"
    titel, episode, more = inputbox("Folgen", "", default_long_text=titel, image_url=image_for_form)
    seen_on = datetime.datetime.now().strftime('%d.%m.%Y')
    log_debug(f"Saving to ODS: titel={titel}, episode={episode}, seen_on={seen_on}, url={url}, more={more}, cover={cover}")
    append_row_to_ods(titel, episode, seen_on, url, more, cover)
    log_debug("Successfully saved to ODS")
    if msg:
        log_debug("Sending response to Chrome")
        send_native_message({"result": "OK"})
        log_debug("Response sent successfully")
    else:
        print("Gespeichert!")
    log_debug("Script completed successfully")
    app = QApplication.instance()
    if app:
        app.quit()