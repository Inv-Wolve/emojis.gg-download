import os
import requests
import json


API_URL = "https://emoji.gg/api"  
DOWNLOAD_FOLDER = "downloaded_emojis"
TRACKER_FILE = "downloaded_emojis.json"
MAX_DOWNLOADS = 500


if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)


if os.path.exists(TRACKER_FILE):
    with open(TRACKER_FILE, "r") as f:
        downloaded_emojis = json.load(f)
else:
    downloaded_emojis = []

def save_tracker():
    with open(TRACKER_FILE, "w") as f:
        json.dump(downloaded_emojis, f)

def get_emojis():
    try:
        response = requests.get(API_URL)
        if response.status_code == 200:
            emojis = response.json()
            emoji_urls = [emoji["image"] for emoji in emojis if not emoji["image"].endswith(".gif")]
            print(f"Fetched {len(emoji_urls)} static emojis from Emoji.gg.")
            return emoji_urls
        else:
            print(f"Failed to fetch emojis. Status code: {response.status_code}")
            return []
    except Exception as e:
        print(f"Error fetching emojis: {e}")
        return []

def download_emoji(url, filename):
    try:
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            with open(filename, "wb") as f:
                f.write(response.content)
            return True
        else:
            print(f"Failed to download {url}, status code {response.status_code}")
            return False
    except Exception as e:
        print(f"Error downloading {url}: {e}")
        return False

def main():
    emoji_urls = get_emojis()
    new_downloads = 0

    for url in emoji_urls:
        if url in downloaded_emojis:
            print(f"Skipping already downloaded emoji: {url}")
            continue

        emoji_name = url.split("/")[-1] 
        filepath = os.path.join(DOWNLOAD_FOLDER, emoji_name)

        if download_emoji(url, filepath):
            print(f"Downloaded {emoji_name}")
            downloaded_emojis.append(url)
            new_downloads += 1

            if new_downloads % 50 == 0:
                save_tracker()
                print("Progress saved to tracker file.")

            if new_downloads >= MAX_DOWNLOADS:
                break
        else:
            print(f"Failed to download {emoji_name}")

    save_tracker()
    print(f"Downloaded {new_downloads} new emojis. Total downloaded emojis tracked: {len(downloaded_emojis)}")

if __name__ == "__main__":
    main()