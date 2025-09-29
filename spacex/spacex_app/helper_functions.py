import requests

def api_request(api_url: str):
    response = requests.get(api_url)
    response.raise_for_status()
    data = response.json()
    return data