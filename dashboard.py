import os
import json
import argparse
import requests
import webbrowser

header_id = 0

def main():
    args = parse_args()
    cfg = load_config(args.get('config',"./config.json"))
    load_dashboard(cfg)
    quit()

def parse_args():
    parser = argparse.ArgumentParser(description = "desc?")
    parser.add_argument("-c","--config", action = "store", default = "config.json", nargs=1, help = "Path for the JSON config file to use.", required=False)
    argdict = {x[0]:x[1] for x in parser.parse_args()._get_kwargs()}
    return argdict

def load_config(cfg_file):
    try:
        with open(cfg_file,'r',encoding='u8') as f:
            cfg = json.load(f)
    except:
        cfg = {}
    # TODO: clean the cfg, make sure all the keys we expect to find are filled out
    return cfg

def load_dashboard(cfg):
    load_accuweather(cfg.get("DEFAULT LOCATION",{}))
    load_flights(cfg.get("DEFAULT LOCATION",{}))
    load_solar_flare()
    load_internet_outages(cfg.get("ISP"))
    load_drive_times(cfg.get("DEFAULT LOCATION",{}))
    load_traffic(cfg.get("DEFAULT LOCATION",{}))
    return None

def load_accuweather(dl_cfg = {}):
    """
    dl_cfg = default location cfg dict
    """
    sites = {
        "quick overview" : f"https://www.accuweather.com/en/us/{dl_cfg['CITY']}/{dl_cfg['ZIPCODE']}/current-weather/{dl_cfg['ACCUWEATHER ID']}",
        "quick overview hourly" : f"https://www.accuweather.com/en/us/{dl_cfg['CITY']}/{dl_cfg['ZIPCODE']}/hourly-weather-forecast/{dl_cfg['ACCUWEATHER ID']}",
        "wind speed" : f"https://www.accuweather.com/en/us/{dl_cfg['STATE']}/wind-flow",
        "air quality" : f"https://www.accuweather.com/en/us/{dl_cfg['CITY']}/{dl_cfg['ZIPCODE']}/air-quality-index/{dl_cfg['ACCUWEATHER ID']}",
        "allergens" : f"https://www.accuweather.com/en/us/{dl_cfg['CITY']}/{dl_cfg['ZIPCODE']}/allergies-weather/{dl_cfg['ACCUWEATHER ID']}?name=tree-pollen",
        "rainfall" : f"https://www.accuweather.com/en/us/{dl_cfg['CITY']}/{dl_cfg['ZIPCODE']}/minute-weather-forecast/{dl_cfg['ACCUWEATHER ID']}",
    }
    
    for key in sites:
        webbrowser.open(sites[key], new=2)
    return

def load_flights(dl_cfg = {}):
    url = f"https://www.flightradar24.com/{dl_cfg['COORDINATES']['LAT']},{dl_cfg['COORDINATES']['LONG']}/14"
    webbrowser.open(url, new=2)

def load_solar_flare():
    url = "spaceweatherlive.com/en/solar-activity/solar-flares.html"
    webbrowser.open(url, new=2)

def load_internet_outages(isp = ""):
    sites = {
        "all" : f"https://downdetector.com/",
        "isp" : f"https://downdetector.com/status/{isp}/"
    }

    for key in sites:
        webbrowser.open(sites[key], new=2)

def load_drive_times(dl_cfg = {}):
    url = "https://app.traveltime.com/search/"
    opts = [{"tt":15,"color":"%23f7941d"}, {"tt":60,"color":"%23d60064"}, {}]
    for i in range(len(opts)):
        url += f"&{i}-lng={dl_cfg['COORDINATES']['LONG']}&{i}-lat={dl_cfg['COORDINATES']['LAT']}&{i}-time=d{int(time.time()*1000)}&{i}-mode=driving"
        if opts[i]:
            for key in opts[i]:
                url += f"&{i}-{key}={opts[i][key]}"
    url += "&selected=0"
    webbrowser.open(url, new=2)

def load_traffic(dl_cfg = {}):
    zoom_level = 13
    url = f"https://www.google.com/maps/@{dl_cfg['COORDINATES']['LAT']},{dl_cfg['COORDINATES']['LONG']},{zoom_level}z/data=!5m1!1e1"
    webbrowser.open(url, new=2)

def get_request(url):
    header = get_a_request_header()
    r = requests.get(url,headers=header)
    return r

def get_a_request_header():
    global header_id
    headers = [
        {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"},
    ]
    header_id = (header_id + 1) % len(headers)
    return headers[header_id]


def DEBUG_set_clipboard_data(text):
    import win32clipboard
    win32clipboard.OpenClipboard()
    try:
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardText(str(text))
    except UnicodeEncodeError as e:
        try:
            win32clipboard.SetClipboardText(str(text), win32clipboard.CF_UNICODETEX)
        except:
            pass
    finally:
        win32clipboard.CloseClipboard()

if __name__ == "__main__":
    main()