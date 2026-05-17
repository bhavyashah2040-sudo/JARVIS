import csv
import sqlite3
import os

con = sqlite3.connect("jarvis.db")
cursor = con.cursor()

# Make sure contacts table exists
cursor.execute("""CREATE TABLE IF NOT EXISTS contacts (
    id integer primary key, 
    name VARCHAR(200), 
    mobile_no VARCHAR(255), 
    email VARCHAR(255), 
    address VARCHAR(255)
)""")

# Read the exported Google CSV
csv_file = "contacts.csv"

if not os.path.exists(csv_file):
    print("ERROR: contacts.csv not found in C:\\Jarvis\\")
    print("Please export from https://contacts.google.com and save as contacts.csv here")
    exit()

added = 0
skipped = 0
no_number = 0

with open(csv_file, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    
    print("CSV Columns found:", reader.fieldnames)
    print("")
    
    for row in reader:
        # Google CSV uses these column names
        # Try multiple possible column names for name and phone
        name = (
            row.get('Name') or 
            row.get('First Name', '') + ' ' + row.get('Last Name', '') or
            row.get('name') or 
            ''
        ).strip()
        
        # Phone number - Google exports multiple phone columns
        phone = (
            row.get('Phone 1 - Value') or
            row.get('Mobile Phone') or
            row.get('Phone') or
            row.get('phone') or
            row.get('Phone 1') or
            ''
        ).strip()
        
        email = (
            row.get('E-mail 1 - Value') or
            row.get('Email') or
            row.get('email') or
            ''
        ).strip()
        
        address = (
            row.get('Address 1 - Formatted') or
            row.get('Address') or
            ''
        ).strip()
        
        # Skip if no name or no phone
        if not name:
            skipped += 1
            continue
            
        if not phone:
            no_number += 1
            print(f"No number for: {name}")
            continue
        
        # Clean phone number - remove spaces, dashes, brackets
        phone = phone.replace(' ', '').replace('-', '').replace('(', '').replace(')', '')
        
        # Skip if contact already exists
        cursor.execute(
            "SELECT id FROM contacts WHERE LOWER(name) = ? OR mobile_no = ?",
            (name.lower(), phone)
        )
        if cursor.fetchone():
            skipped += 1
            continue
        
        # Insert into database
        cursor.execute(
            "INSERT INTO contacts VALUES (null, ?, ?, ?, ?)",
            (name, phone, email, address)
        )
        added += 1
        print(f"Added: {name} - {phone}")

con.commit()
con.close()

print(f"\n=== DONE ===")
print(f"Added:    {added} contacts")
print(f"Skipped:  {skipped} (already exist or no name)")
print(f"No phone: {no_number} contacts had no number")
print(f"\nYou can now say 'call [name]' in Jarvis!")
