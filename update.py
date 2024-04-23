import requests
import os
CURRENT_VERSION = "V1.00.02X"
UPDATE_URL = "https://raw.githubusercontent.com/MakxXun/Arthanoid-Systems/main/GeneralTestingV"
UPDATE_FILE = "update.py"  # Downloaded update filename

def fetch_latest_version():
    try:
        response = requests.get(UPDATE_URL)
        if response.status_code == 200:
            return response.text.strip()
        else:
            print("Failed to fetch latest version information.")
    except Exception as e:
        print("Error occurred while fetching latest version:", e)
    return None

# Function to check for updates
def check_for_updates():
    latest_version = fetch_latest_version()
    if latest_version:
        if latest_version == CURRENT_VERSION:
            print("You are using the latest version.")
        else:
            print("An update is available.")
            download_update(, )
    else:
        print("Failed to fetch latest version information.")

def download_update(update_url):
  try:
    response = requests.get(update_url, stream=True)
    if response.status_code == 200:
      # Get the current script's path
      current_script_path = os.path.abspath(__file__)
      # Extract the directory path from the script path
      download_path = os.path.dirname(current_script_path)
      # Combine directory path with the desired filename (update.py)
      update_file_path = os.path.join(download_path, "update.py")
      with open(update_file_path, 'wb') as f:
        for chunk in response.iter_content(1024):
          f.write(chunk)
      print("Update downloaded successfully!")
      return True
    else:
      print(f"Failed to download update file. Status code: {response.status_code}")
  except Exception as e:
    print(f"Error occurred while downloading update: {e}")
  return False

def install_update(update_path, current_script_path):
    try:
        if os.path.exists(update_path):
        os.replace(update_path, current_script_path)
        print("Update installed successfully!")
        return True
        else:
        print("Update file not found.")
    except Exception as e:
        print(f"Error occurred while installing update: {e}")
    return False





