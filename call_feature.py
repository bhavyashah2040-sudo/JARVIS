import os
import re
import time
import subprocess
import eel
import sqlite3

PHONE_IP = "10.81.50.211"  # Your phone's IP
ADB_PORT = "5555"

con = sqlite3.connect("jarvis.db")
cursor = con.cursor()

def ensure_adb_connected():
    """Make sure ADB is connected to phone before any command"""
    # Check if device is connected
    result = subprocess.run(['adb', 'devices'], capture_output=True, text=True)
    print(f"[ADB] Devices: {result.stdout}")
    
    if PHONE_IP not in result.stdout:
        print(f"[ADB] Reconnecting to {PHONE_IP}:{ADB_PORT}...")
        subprocess.run(['adb', 'connect', f'{PHONE_IP}:{ADB_PORT}'], 
                      capture_output=True, text=True)
        time.sleep(2)
        
        # Check again
        result = subprocess.run(['adb', 'devices'], capture_output=True, text=True)
        if PHONE_IP in result.stdout:
            print("[ADB] Reconnected successfully!")
            return True
        else:
            print("[ADB] Could not reconnect!")
            return False
    return True

def extract_number(text):
    """Extract phone number from user text"""
    number = re.sub(r'[\s\-\(\)]', '', text)
    match = re.search(r'(\+?\d{10,13})', number)
    return match.group(1) if match else None

def call_by_number(number):
    """Make a call to a specific number via ADB"""
    number = number.replace(" ", "").replace("-", "")
    if not number.startswith('+'):
        number = '+91' + number
    
    print(f"[Call] Calling {number}")
    
    # Always reconnect before calling
    connected = ensure_adb_connected()
    if not connected:
        print("[Call] ADB not connected, trying anyway...")
    
    result = subprocess.run(
        ['adb', 'shell', 'am', 'start', '-a', 
         'android.intent.action.CALL', '-d', f'tel:{number}'],
        capture_output=True, text=True
    )
    print(f"[Call] Result: {result.stdout} {result.stderr}")

def call_by_name(name):
    """Look up contact by name and call"""
    try:
        name = name.strip().lower()
        cursor.execute(
            "SELECT name, mobile_no FROM contacts WHERE LOWER(name) LIKE ?",
            ('%' + name + '%',)
        )
        results = cursor.fetchall()
        if results:
            contact_name, number = results[0]
            return contact_name, number
        return None, None
    except:
        return None, None

@eel.expose
def handleCallCommand(query):
    """Main call handler"""
    from engine.command import speak, takecommand

    query = query.lower().strip()

    # Remove trigger words
    for word in ['call', 'dial', 'phone', 'ring', 'jarvis']:
        query = query.replace(word, '').strip()

    query = query.strip()

    if not query:
        speak("Who should I call? Please say a name or number.")
        response = takecommand()
        if not response:
            speak("I could not hear. Please try again.")
            return
        query = response.strip()

    # Check if it looks like a number
    number = extract_number(query)

    if number:
        speak(f"Calling {number}")
        call_by_number(number)
    else:
        # Try to find in contacts by name
        contact_name, number = call_by_name(query)
        if contact_name and number:
            speak(f"Calling {contact_name}")
            call_by_number(number)
        else:
            speak(f"I could not find {query} in contacts. Please say the number.")
            response = takecommand()
            if response:
                number = extract_number(response)
                if number:
                    speak(f"Calling {number}")
                    call_by_number(number)
                else:
                    speak("Sorry, I could not understand the number.")
            else:
                speak("I could not hear the number. Please try again.")
