import requests

url = "https://machine-learning-deployment-74qf.onrender.com/predict"

voter_data = {
    # 1. LOCATION FIRST (Since Gender-first failed, this is the likely correct order)
    "latitude": 12.9716, 
    "longitude": 77.5946,

    # 2. GENDER LAST (Strictly Alphabetical: F -> M -> P)
    "gender_Female": 0,
    "gender_Male": 1,
    "gender_Polygender": 0
    
    # REMOVED: "gender_Bigender" (The model explicitly rejected this)
}

print(f"Sending checking request to: {url}...")

try:
    response = requests.post(url, json=voter_data)
    
    if response.status_code == 200:
        result = response.json()
        print("\n✅ SUCCESS! The Detective replied:")
        print(f"Prediction: {result['prediction']}")
    else:
        print("\n❌ THE KITCHEN FAILED:")
        print(f"Error Code: {response.status_code}")
        # This prints the specific error from the server
        print(f"Message: {response.text}")

except Exception as e:
    print(f"\n⚠️ CONNECTION ERROR: {e}")