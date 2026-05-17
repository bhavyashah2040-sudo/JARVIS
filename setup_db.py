import sqlite3
import os

con = sqlite3.connect("jarvis.db")
cursor = con.cursor()

# Create tables if they don't exist
cursor.execute("""CREATE TABLE IF NOT EXISTS sys_command(
    id integer primary key, 
    name VARCHAR(100), 
    path VARCHAR(1000)
)""")

cursor.execute("""CREATE TABLE IF NOT EXISTS web_command(
    id integer primary key, 
    name VARCHAR(100), 
    url VARCHAR(1000)
)""")

cursor.execute("""CREATE TABLE IF NOT EXISTS contacts(
    id integer primary key, 
    name VARCHAR(200), 
    mobile_no VARCHAR(255), 
    email VARCHAR(255), 
    address VARCHAR(255)
)""")

cursor.execute("""CREATE TABLE IF NOT EXISTS info(
    name VARCHAR(100), 
    designation VARCHAR(50),
    mobileno VARCHAR(40), 
    email VARCHAR(200), 
    city VARCHAR(300)
)""")

# Common web commands
web_commands = [
    ('whatsapp', 'https://web.whatsapp.com/'),
    ('youtube', 'https://www.youtube.com/'),
    ('google', 'https://www.google.com/'),
    ('gmail', 'https://mail.google.com/'),
    ('instagram', 'https://www.instagram.com/'),
    ('facebook', 'https://www.facebook.com/'),
    ('twitter', 'https://www.twitter.com/'),
    ('github', 'https://www.github.com/'),
    ('netflix', 'https://www.netflix.com/'),
    ('chatgpt', 'https://chat.openai.com/'),
]

# Common system commands (update paths if different on your PC)
sys_commands = [
    ('notepad', 'notepad.exe'),
    ('calculator', 'calc.exe'),
    ('paint', 'mspaint.exe'),
    ('task manager', 'taskmgr.exe'),
    ('file explorer', 'explorer.exe'),
    ('vs code', r'C:\Users\%USERNAME%\AppData\Local\Programs\Microsoft VS Code\Code.exe'),
    ('chrome', r'C:\Program Files\Google\Chrome\Application\chrome.exe'),
    ('brave', r'C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe'),
]

# Insert web commands (skip if already exist)
for name, url in web_commands:
    cursor.execute("SELECT id FROM web_command WHERE name=?", (name,))
    if not cursor.fetchone():
        cursor.execute("INSERT INTO web_command VALUES (null, ?, ?)", (name, url))
        print(f"Added web: {name}")
    else:
        print(f"Already exists: {name}")

# Insert sys commands (skip if already exist)
for name, path in sys_commands:
    cursor.execute("SELECT id FROM sys_command WHERE name=?", (name,))
    if not cursor.fetchone():
        cursor.execute("INSERT INTO sys_command VALUES (null, ?, ?)", (name, path))
        print(f"Added sys: {name}")
    else:
        print(f"Already exists: {name}")

con.commit()
con.close()
print("\nDatabase setup complete!")
print("You can now say: 'open whatsapp', 'open youtube', 'open chrome' etc.")
