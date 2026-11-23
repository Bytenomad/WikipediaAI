#!/usr/bin/env python3

import requests
import json

# Make a simple request to see the actual response structure
response = requests.post(
    "http://localhost:11434/api/embeddings",
    json={
        "model": "nomic-embed-text",
        "prompt": "This is a test sentence for embedding."
    }
)

print("Status Code:", response.status_code)
print("Response Text:", response.text[:500] + "..." if len(response.text) > 500 else response.text)

if response.status_code == 200:
    try:
        data = response.json()
        print("\nJSON Response Structure:")
        print(json.dumps(data, indent=2))
        print("\nKeys in response:", list(data.keys()))
        if 'embedding' in data:
            print("Embedding type:", type(data['embedding']))
            print("Embedding length:", len(data['embedding']) if isinstance(data['embedding'], (list, tuple)) else "N/A")
    except Exception as e:
        print("Error parsing JSON:", e)