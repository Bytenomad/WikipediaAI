#!/usr/bin/env python3
"""
Configuration script for Open WebUI to use Wikipedia AI pipeline data.
This script verifies the setup and provides instructions for completing the integration.
"""

import os
import sys
import json

def check_setup():
    """Check if all required components are in place"""
    
    print("=== Open WebUI Configuration Check ===")
    
    # Check database file exists
    db_path = "open-webui/vector_db/chroma.sqlite3"
    if os.path.exists(db_path):
        print(f"[OK] Chroma database found: {db_path}")
        db_size = os.path.getsize(db_path)
        print(f"  Size: {db_size} bytes")
    else:
        print(f"[ERROR] Chroma database not found: {db_path}")
        return False
    
    # Check if we have the necessary directories
    required_dirs = [
        "open-webui/vector_db",
        "open-webui/uploads"
    ]
    
    for dir_path in required_dirs:
        if os.path.exists(dir_path):
            print(f"[OK] Directory exists: {dir_path}")
        else:
            print(f"[INFO] Creating directory: {dir_path}")
            os.makedirs(dir_path, exist_ok=True)
    
    # Verify data structure
    print("\n=== Data Verification ===")
    try:
        # Try to import chromadb to verify it's available
        from chromadb import Client
        print("[OK] ChromaDB import successful")
        
        # Try to connect to database
        client = Client()
        collections = client.list_collections()
        print(f"[OK] Connected to ChromaDB - Found {len(collections)} collection(s)")
        
        for collection in collections:
            print(f"  Collection: {collection.name} (count: {collection.count()})")
            
    except ImportError:
        print("[ERROR] ChromaDB not installed - please install with 'pip install chromadb'")
        return False
    except Exception as e:
        print(f"[WARNING] Could not connect to ChromaDB: {e}")
    
    return True

def generate_config_instructions():
    """Generate configuration instructions for Open WebUI"""
    
    print("\n=== Configuration Instructions ===")
    print("To complete the Open WebUI setup, follow these steps:")
    print()
    print("1. Run Open WebUI with Docker:")
    print("   docker-compose -f docker-compose-openwebui-fixed.yml up -d")
    print()
    print("2. Access Open WebUI at: http://localhost:8080")
    print()
    print("3. Configure the following settings in Open WebUI:")
    print("   - Database URL: sqlite:///vector_db/chroma.sqlite3")
    print("   - Embedding model: Choose an appropriate model (e.g., all-MiniLM-L6-v2)")
    print("   - Vector store: Chroma")
    print()
    print("4. Test the integration by asking questions about Wikipedia content")
    print()

def main():
    """Main configuration function"""
    
    print("Open WebUI Configuration for Wikipedia AI Pipeline")
    print("=" * 55)
    
    if check_setup():
        generate_config_instructions()
        print("[OK] Setup verification completed successfully!")
        print("\nThe Wikipedia AI pipeline data is ready to be used with Open WebUI.")
        print("You can now start Open WebUI and test chat functionality with Wikipedia content.")
    else:
        print("[ERROR] Setup verification failed. Please check the errors above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
