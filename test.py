import requests

# URL of your FastAPI application
BASE_URL = "http://127.0.0.1:8000"

def request_scatter_plot():
    response = requests.get(f"{BASE_URL}/scatter-plot")
    if response.status_code == 200:
        print("Scatter Plot Response:")
        print(response.json())
    else:
        print("Failed to generate scatter plot.")
        print(f"Status Code: {response.status_code}, Response: {response.text}")

def request_map():
    response = requests.get(f"{BASE_URL}/map")
    if response.status_code == 200:
        print("Map Response:")
        print(response.json())
    else:
        print("Failed to generate map.")
        print(f"Status Code: {response.status_code}, Response: {response.text}")

if __name__ == "__main__":
    request_scatter_plot()
    request_map()
