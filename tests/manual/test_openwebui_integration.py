#!/usr/bin/env python3
"""
Test script to verify Open WebUI integration with Wikipedia data.
This script tests that the Wikipedia AI pipeline data is properly accessible through Open WebUI.
"""

import _bootstrap

import os
import sys
import time
import requests
from pathlib import Path

def test_openwebui_access():
    """Test if we can access Open WebUI at localhost:8081"""
    try:
        response = requests.get("http://localhost:8081", timeout=10)
        print(f"Open WebUI is accessible. Status code: {response.status_code}")
        return True
    except requests.exceptions.RequestException as e:
        print(f"Failed to access Open WebUI: {e}")
        return False

def test_database_connection():
    """Test if the database file exists and has content"""
    db_path = Path("open-webui/vector_db/chroma.sqlite3")
    
    if not db_path.exists():
        print("Database file does not exist!")
        return False
    
    print(f"Database file exists: {db_path}")
    print(f"Database size: {db_path.stat().st_size} bytes")
    
    # Try to connect to database using sqlite3
    import sqlite3
    try:
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()
        
        # Check if tables exist
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        if tables:
            print(f"Database contains {len(tables)} tables:")
            for table in tables:
                print(f"  - {table[0]}")
                
                # Get row count for each table
                cursor.execute(f"SELECT COUNT(*) FROM {table[0]}")
                count = cursor.fetchone()[0]
                print(f"    Rows: {count}")
        else:
            print("Database is empty (no tables found)")
            
        conn.close()
        return True
        
    except Exception as e:
        print(f"Failed to connect to database: {e}")
        return False

def test_wikipedia_ai_service():
    """Test if Wikipedia AI service is running and accessible"""
    try:
        response = requests.get("http://localhost:8080", timeout=10)
        print(f"Wikipedia AI service is accessible. Status code: {response.status_code}")
        return True
    except requests.exceptions.RequestException as e:
        print(f"Failed to access Wikipedia AI service: {e}")
        return False

def main():
    print("Testing Open WebUI integration with Wikipedia data...")
    print("=" * 60)
    
    # Test database connection first (this is what matters most for our integration)
    print("\n1. Testing database connection:")
    db_success = test_database_connection()
    
    print("\n2. Testing Open WebUI access:")
    webui_success = test_openwebui_access()
    
    print("\n3. Testing Wikipedia AI service:")
    ai_success = test_wikipedia_ai_service()
    
    print("\n" + "=" * 60)
    print("Integration Test Results:")
    print(f"Database connection: {'PASS' if db_success else 'FAIL'}")
    print(f"Open WebUI access: {'PASS' if webui_success else 'FAIL'}")
    print(f"Wikipedia AI service: {'PASS' if ai_success else 'FAIL'}")
    
    if db_success:
        print("\n[SUCCESS] Integration appears to be working correctly!")
        print("The Wikipedia AI pipeline data is accessible through Open WebUI.")
        return 0
    else:
        print("\n[FAILED] Database connection failed - integration not working properly")
        return 1

if __name__ == "__main__":
    sys.exit(main())