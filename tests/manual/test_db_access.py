
import _bootstrap
import os
import sqlite3
from pathlib import Path

# Test if we can access the database file directly
db_path = Path("open-webui/vector_db/chroma.sqlite3")

print(f"Database path: {db_path.absolute()}")
print(f"Database exists: {db_path.exists()}")

if db_path.exists():
    try:
        # Try to connect to the database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # List tables to verify it's a proper database
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        print(f"Database tables: {tables}")
        print("Successfully connected to the database!")
        
        conn.close()
    except Exception as e:
        print(f"Error connecting to database: {e}")
else:
    print("Database file does not exist!")

# Also check file permissions
try:
    stat = os.stat(db_path)
    print(f"File size: {stat.st_size} bytes")
    print(f"File permissions: {oct(stat.st_mode)}")
except Exception as e:
    print(f"Error getting file info: {e}")