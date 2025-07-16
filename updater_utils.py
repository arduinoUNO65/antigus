# updater_utils.py
# Utility functions for updating virus definitions
import requests

def fetch_definitions(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text.splitlines()
        else:
            print(f"Failed to fetch definitions: {response.status_code}")
            return []
    except Exception as e:
        print(f"Error fetching definitions: {e}")
        return []
