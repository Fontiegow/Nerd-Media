import requests

def get_steam_app_list():
    url = "http://api.steampowered.com/ISteamApps/GetAppList/v2/"

    headers = {
        "User-Agent": "Mozilla/5.0 (SteamDataResearcher/1.0)"
    }

    try:
        req = requests.get(url, headers=headers, timeout=15)
        req.raise_for_status()
        return req.json()
    except requests.RequestException as e:
        print(f"Failed to get all games on Steam: {e}")
        return None

apps = get_steam_app_list()

if apps:
    print(len(apps["applist"]["apps"]))
