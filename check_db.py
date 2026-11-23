#!/usr/bin/env python3
"""
Check Chroma database connection.
"""

import sys
sys.path.insert(0, 'src')

# Test Chroma database access
try:
    from chromadb import Client
    
    print('Testing Chroma connection...')
    client = Client()
    print('SUCCESS: Chroma client created')
    
    collections = client.list_collections()
    print('Collections found: ' + str(len(collections)))
    
    if len(collections) > 0:
        for collection in collections:
            print('Collection name: ' + collection.name)
            print('Collection count: ' + str(collection.count()))
    else:
        print('No collections found')
        
except Exception as e:
    print('ERROR: ' + str(e))
    import traceback
    traceback.print_exc()