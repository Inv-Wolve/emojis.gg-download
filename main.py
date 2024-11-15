import os
import requests
import json
import re 

API_URL = "https://emoji.gg/api"
DOWNLOAD_FOLDER = "downloaded_emojis"
TRACKER_FILE = "downloaded_emojis.json"
MAX_DOWNLOADS = 500
filter_18_keywords_yes = {"yes", "y", "agree", "block", "on", "allow", "filter"}
filter_18_keywords_no = {"no", "n", "disagree", "off", "allowlist", "unblock", "don't", "dont", "nah", "niet"}

def get_user_input():
    while True:
        filter_18 = input('Should 18+ stuff be blocked? (y/n): ').strip().lower()
        if filter_18 in filter_18_keywords_yes:
            return True
        elif filter_18 in filter_18_keywords_no:
            return False
        else:
            print("Invalid input. Please enter 'y' or 'n'.")

adult_keywords = [
    "18+", "18", "adult", "sex", "porn", "nsfw", "xxx", "erotic", "fetish", "boobs", 
    "ass", "fuck", "nude", "nudity", "uncensored", "orgy", "masturbation", "bare", "gay", 
    "lesbian", "hentai", "bikini", "vulgar", "graphic", "gore", "piercing", "fetishism",
    "mature", "explicit", "porno", "cum", "sexy", "dirty", "racy", "stimulation", "fetishist",
    "kink", "busty", "sexually", "horny", "lick", "bondage", "xxx", "xxxvideo", "pornhub", 
    "slut", "whore", "fetishistic", "nipple", "cunt", "tits", "dildo", "pussy", "cock", "penis", 
    "vagina", "squirting", "orgasm", "pornstar", "hardcore", "naked", "stiff", "playboy", 
    "playgirl", "dungeon", "stripper", "seduction", "seductive", "private", "fap", "fapping", 
    "hardcore", "threesome", "cumshot", "cream pie", "peep show", "shower sex", "anal", "shemale", 
    "transsexual", "twink", "milf", "cougar", "dirty talk", "lingerie", "sado-masochism", 
    "dominatrix", "submissive", "dominant", "vibrator", "selfie", "gagging", "pornography", "xxxmovie", 
    "strippers", "blowjob", "boobjob", "fuckable", "deepthroat", "perversion", "rough sex", "spanking", 
    "incest", "rape", "pedophile", "munchkin", "granny", "lesbian sex", "sexting", "fleshlight", "double penetration", 
    "golden shower", "gangbang", "cumdump", "cumslut", "slutty", "choking", "sloppy", "penis enlargement", 
    "scissoring", "facefucking", "tease", "nipple play", "exhibitionism", "voyeurism", "mature milf", "cumtribute", 
    "hotwife", "fisting", "bdsm", "dirty pictures", "naughty", "naked", "orgasming", "strip tease", "booty", 
    "climax", "fucked", "twerking", "asshole", "assplay", "hotandheavy", "sex addict", "self pleasure", 
    "dirty videos", "face sitting", "girl on girl", "boy on boy", "slutty girl", "gagging on cock", "degrading", 
    "toys", "adult toys", "gangbang", "anal beads", "cherry popping", "group sex", "masturbate", "latex", "bondage gear",
    "sex tape", "pornographic", "fuck fest", "oral sex", "sex game", "sexual fantasy", "deep penetration", 
    "anal sex", "vibrator play", "rough anal", "kinky sex", "pubes", "hotwife", "pornographic movie", "dirty scenes"
]


adult_pattern = re.compile(r'|'.join([re.escape(keyword) for keyword in adult_keywords]), re.IGNORECASE)

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

def contains_18_plus(url):
    return bool(adult_pattern.search(url))

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
    filter_18 = get_user_input()  
    emoji_urls = get_emojis()
    new_downloads = 0

    for url in emoji_urls:
        if url in downloaded_emojis:
            print(f"Skipping already downloaded emoji: {url}")
            continue
        
        if filter_18 and contains_18_plus(url):
            print(f"Skipping emoji due to 18+ content: {url}")
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