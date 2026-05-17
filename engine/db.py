import sqlite3

con = sqlite3.connect("jarvis.db")
cursor = con.cursor()

# Check all tables exist
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()
print("=== TABLES ===")
for t in tables:
    print(t[0])

print("\n=== WEB COMMANDS ===")
try:
    cursor.execute("SELECT * FROM web_command")
    rows = cursor.fetchall()
    if rows:
        for r in rows:
            print(r)
    else:
        print("EMPTY - no web commands found!")
except Exception as e:
    print("Error:", e)

print("\n=== SYS COMMANDS ===")
try:
    cursor.execute("SELECT * FROM sys_command")
    rows = cursor.fetchall()
    if rows:
        for r in rows:
            print(r)
    else:
        print("EMPTY - no sys commands found!")
except Exception as e:
    print("Error:", e)

con.close()
