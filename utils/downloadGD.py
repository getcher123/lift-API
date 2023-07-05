import requests

def download_google_drive_json_file(id: str) -> dict:
    url = f"https://drive.google.com/uc?id={id}&export=download"
    response = requests.get(url)
    response.raise_for_status()
    json_data = response.json()
    return json_data