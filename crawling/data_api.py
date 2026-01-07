import requests
import json

# --- CONFIGURATION ---
API_KEY = 'GJ2YSMXQC9ZSM29KLKNYQFCV5'
CITY = "Ha noi"
START_DATE = "2023-01-01"
END_DATE = "2023-01-05"

# Generate output filename
filename = f"weather_{CITY}_{START_DATE}_{END_DATE}.json"

def download_json_file():
    # API Endpoint URL
    url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{CITY}/{START_DATE}/{END_DATE}"
    
    params = {
        "unitGroup": "metric",
        "key": API_KEY,
        "include": "hours",
        "contentType": "json"
    }

    print(f"Downloading data to {filename}...")
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        
        # Get JSON content
        data = response.json()
        
        # --- SAVE FILE ---
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
            
        print("Done! File saved successfully.")
        
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    download_json_file()
