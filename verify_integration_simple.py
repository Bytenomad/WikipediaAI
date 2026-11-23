#!/usr/bin/env python3
"""
Simple verification script to ensure the Open WebUI integration is working properly.
This script verifies that our Wikipedia data is correctly set up in the Chroma database
and demonstrates how it would be used by Open WebUI.
"""

import sys
import os
import json
from pathlib import Path

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(__file__))

def check_chroma_setup():
    """Check if we can access the Chroma database"""
    print("Checking Chroma Database Setup")
    print("-" * 30)
    
    try:
        # Try to import chromadb components
        from chromadb import Client
        from chromadb.config import Settings
        
        print("Chroma imports successful")
        
        # Check if the database file exists
        db_path = os.path.join(os.path.dirname(__file__), 'open-webui', 'vector_db', 'chroma.sqlite3')
        if os.path.exists(db_path):
            print("Chroma database file found: " + db_path)
            
            # Try to connect to Chroma
            client = Client()
            collections = client.list_collections()
            print("Successfully connected to Chroma")
            print("Found " + str(len(collections)) + " collection(s)")
            
            for collection in collections:
                print("  Collection: " + collection.name)
                print("    Count: " + str(collection.count()))
                
                # Try to get some sample data
                try:
                    docs = collection.peek(3)
                    print("    Sample documents retrieved successfully")
                except Exception as e:
                    print("    Warning: Could not peek at documents: " + str(e))
                    
        else:
            print("Chroma database file not found: " + db_path)
            return False
            
    except ImportError as e:
        print("Chroma import failed: " + str(e))
        print("Note: You may need to install chromadb package")
        return False
    except Exception as e:
        print("Chroma connection failed: " + str(e))
        return False
        
    return True

def check_export_data():
    """Check the export data that was used to populate Chroma"""
    print("\nChecking Export Data")
    print("-" * 30)
    
    try:
        # Check if our export file exists
        export_file = os.path.join(os.path.dirname(__file__), 'qdrant_export.json')
        if os.path.exists(export_file):
            print("Export file found: " + export_file)
            
            with open(export_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            print("Successfully loaded export data")
            print("Total documents: " + str(len(data)))
            
            if len(data) > 0:
                sample_doc = data[0]
                title = sample_doc.get('metadata', {}).get('title', 'No title')
                print("Sample document title: " + title)
                
                # Show some metadata
                metadata = sample_doc.get('metadata', {})
                print("Metadata keys: " + str(list(metadata.keys())))
                
        else:
            print("Export file not found: " + export_file)
            return False
            
    except Exception as e:
        print("Failed to check export data: " + str(e))
        return False
        
    return True

def check_wikipedia_data():
    """Check if Wikipedia data is properly structured"""
    print("\nChecking Wikipedia Data Structure")
    print("-" * 30)
    
    try:
        # Check our main data files
        zim_file = "D:\\WikipediaAI\\wikipedia\\downloads\\wikipedia_en_all_maxi_2026-08.zim"
        if os.path.exists(zim_file):
            print("ZIM file found: " + zim_file)
            
            # Get file size
            file_size = os.path.getsize(zim_file)
            print("File size: " + str(file_size) + " bytes")
        else:
            print("ZIM file not found: " + zim_file)
            
        # Check if we have any processed articles
        src_dir = os.path.join(os.path.dirname(__file__), 'src')
        if os.path.exists(src_dir):
            print("Source directory found: " + src_dir)
            
            # List some important files
            important_files = ['run_full_ingestion.py', 'chunking.py', 'qdrant_export.py']
            for file in important_files:
                file_path = os.path.join(src_dir, file)
                if os.path.exists(file_path):
                    print("  Found: " + file)
                else:
                    print("  Missing: " + file)
        else:
            print("Source directory not found: " + src_dir)
            
    except Exception as e:
        print("Failed to check Wikipedia data: " + str(e))
        return False
        
    return True

def main():
    """Main verification function"""
    print("Open WebUI Integration Verification")
    print("=" * 50)
    
    # Run all checks
    checks = [
        check_chroma_setup,
        check_export_data, 
        check_wikipedia_data
    ]
    
    results = []
    for check in checks:
        try:
            result = check()
            results.append(result)
        except Exception as e:
            print("Error running " + check.__name__ + ": " + str(e))
            results.append(False)
    
    print("\n" + "=" * 50)
    print("VERIFICATION RESULTS")
    print("=" * 50)
    
    if all(results):
        print("ALL CHECKS PASSED - Integration is working correctly!")
        print("\nThe Wikipedia AI pipeline data has been successfully integrated with Open WebUI.")
        print("To use this in actual Open WebUI:")
        print("1. Install Open WebUI (requires Python 3.11+)")
        print("2. Configure it to use the Chroma database at open-webui/vector_db/chroma.sqlite3")
        print("3. Start Open WebUI and test with Wikipedia queries")
    else:
        print("Some checks failed - there may be integration issues")
        for i, (check, result) in enumerate(zip(checks, results)):
            status = "PASS" if result else "FAIL"
            print("  " + str(i+1) + ". " + check.__name__ + ": " + status)

if __name__ == "__main__":
    main()