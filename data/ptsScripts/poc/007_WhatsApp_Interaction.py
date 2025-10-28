'''
@name: 
@author: kayma
@createdon: "2025-10-25"
@description:
'''

__created__ = "2025-10-25"
__updated__ = "2025-10-25"
__author__  = "kayma"

import webbrowser
import time
import urllib.parse
from ahk import AHK

ahk = AHK()

def send_whatsapp_message(phone_number: str, message: str, timeout: int = 25):
    """
    Opens WhatsApp Web/Desktop for the given number and auto-sends the message.
    - Unicode-safe for any language or emoji
    - Dynamically focuses message box
    - Optionally closes the tab/browser after sending
    """

    # --- Prepare URL (Unicode safe) ---
    phone_number = phone_number.replace(" ", "").replace("+", "")
    encoded_message = urllib.parse.quote(message, safe="")
    url = f"https://api.whatsapp.com/send?phone={phone_number}&text={encoded_message}"
    print(f"Opening WhatsApp chat: {url}")
    webbrowser.open(url)

    # --- Wait for window ---
    print("Waiting for WhatsApp window to appear...")
    start_time = time.time()
    win = None
    titles = [
        "WhatsApp",
        "WhatsApp - Google Chrome",
        "WhatsApp - Microsoft Edge",
        "WhatsApp Web",
        "WhatsApp - Brave"
    ]

    while time.time() - start_time < timeout:
        for title in titles:
            win = ahk.win_get(title=title)
            if win:
                break
        if win:
            print(f"WhatsApp window detected: {win.title}")
            break
        time.sleep(1)

    if not win:
        print("WhatsApp window not found within timeout.")
        return False

    # --- Focus ---
    win.activate()
    time.sleep(0.8)
    try:
        win.always_on_top = 1
        time.sleep(0.3)
        win.always_on_top = 0
        time.sleep(0.5)
    except Exception as e:
        print("Couldn't toggle always_on_top:", e)

    # --- Dynamic click to focus message box ---
    try:
        x, y, width, height = win.get_position()
    except AttributeError:
        x, y, width, height = win.win_get_pos()

    x_focus = x + width // 2
    y_focus = y + int(height * 0.88)
    ahk.mouse_move(x_focus, y_focus, speed=10)
    ahk.click()
    time.sleep(0.6)

    # --- Press Enter ---
    ahk.key_press('Enter')
    print("Message sent (Enter key delivered).")

    return True

send_whatsapp_message("+917904897109", "yhjuik")
