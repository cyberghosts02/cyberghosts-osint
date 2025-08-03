#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
CYBER GHOST OSINT SUITE
Developer: CYBER ALPHA
Description: Insane-level OSINT toolkit with Tor integration, proxy fallback, and 13 modules.
Educational use only.
"""

import os
import sys
import subprocess
import time
import threading
import requests
import socket
from datetime import datetime
from bs4 import BeautifulSoup
from colorama import Fore, Style, init
from stem import Signal
from stem.control import Controller

# Auto install dependencies if missing
required_libs = ["requests", "bs4", "colorama", "stem", "pillow"]
for lib in required_libs:
    try:
        __import__(lib if lib != "bs4" else "bs4")
    except ImportError:
        print(f"[!] Installing missing library: {lib}")
        subprocess.run([sys.executable, "-m", "pip", "install", lib])

init(autoreset=True)

REPORTS_DIR = "reports"
TOR_PORT = 9050
TOR_CONTROL_PORT = 9051
TOR_PASSWORD = ""  # empty means no auth

if not os.path.exists(REPORTS_DIR):
    os.makedirs(REPORTS_DIR)

# Banner
def banner(tor_status):
    os.system("cls" if os.name == "nt" else "clear")
    print(Fore.RED + r"""
    ______   ______   _  __
  / ____/  / ____/  | |/ /
 / /      / / __    |   / 
/ /___   / /_/ /   /   |  
\____/   \____/   /_/|_|  
                          
    """ + Style.RESET_ALL)
    print(Fore.CYAN + f"Developer: CYBER ALPHA | Team: CYBER GHOST")
    print(Fore.GREEN + f"Tor Connection: {'✅ Active' if tor_status else '❌ Not Active'}")
    print(Style.RESET_ALL)

# Tor functions
def is_tor_running():
    try:
        proxies = {'http': f'socks5h://127.0.0.1:{TOR_PORT}', 'https': f'socks5h://127.0.0.1:{TOR_PORT}'}
        r = requests.get("https://check.torproject.org", proxies=proxies, timeout=10)
        return "Congratulations. This browser is configured to use Tor" in r.text
    except:
        return False

def start_tor():
    if is_tor_running():
        return True
    print("[*] Starting Tor service...")
    try:
        subprocess.Popen(["tor"])
    except FileNotFoundError:
        print("[!] Tor not found. Installing Tor...")
        if "termux" in sys.executable:
            os.system("pkg install tor -y")
        elif sys.platform.startswith("linux"):
            os.system("sudo apt install tor -y")
        elif sys.platform == "darwin":
            os.system("brew install tor")
        else:
            print("[!] Please install Tor manually.")
            return False
        subprocess.Popen(["tor"])
    time.sleep(10)
    return is_tor_running()

def renew_tor_ip():
    try:
        with Controller.from_port(port=TOR_CONTROL_PORT) as controller:
            if TOR_PASSWORD:
                controller.authenticate(password=TOR_PASSWORD)
            else:
                controller.authenticate()
            controller.signal(Signal.NEWNYM)
            print("[*] Tor IP renewed")
    except Exception as e:
        print(f"[!] Failed to renew Tor IP: {e}")

# Proxy list
def get_proxies():
    try:
        r = requests.get("https://www.proxy-list.download/api/v1/get?type=https", timeout=10)
        return r.text.strip().split("\r\n")
    except:
        return []
proxies_list = get_proxies()

# Save reports
def save_report(module_name, content):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = os.path.join(REPORTS_DIR, f"{module_name}_{timestamp}.txt")
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)
    print(Fore.GREEN + f"[+] Report saved to {filename}")

# ===== Module Implementations =====

# --- Username Scanner ---
def username_scanner():
    username = input(Fore.CYAN + "Enter username: ").strip()
    if not username:
        print(Fore.RED + "[!] Empty username.")
        return
    sites = [
        f"https://github.com/{username}",
        f"https://twitter.com/{username}",
        f"https://instagram.com/{username}",
        f"https://facebook.com/{username}",
        f"https://t.me/{username}"
    ]
    found = []
    proxies = {'http': f'socks5h://127.0.0.1:{TOR_PORT}',
               'https': f'socks5h://127.0.0.1:{TOR_PORT}'} if is_tor_running() else None
    def check(url):
        try:
            res = requests.get(url, proxies=proxies, timeout=8)
            if res.status_code == 200:
                found.append(url)
                print(Fore.GREEN + f"[FOUND] {url}")
        except:
            pass
    threads = []
    for s in sites:
        t = threading.Thread(target=check, args=(s,))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()
    save_report("username_scanner", "\n".join(found) if found else "No profiles found.")

# --- IP Geolocation ---
def ip_geolocation():
    ip = input(Fore.CYAN + "Enter IP: ").strip()
    if not ip:
        return
    try:
        proxies = {'http': f'socks5h://127.0.0.1:{TOR_PORT}',
                   'https': f'socks5h://127.0.0.1:{TOR_PORT}'} if is_tor_running() else None
        r = requests.get(f"http://ip-api.com/json/{ip}", proxies=proxies, timeout=8)
        save_report("ip_geolocation", r.text)
    except Exception as e:
        print(Fore.RED + f"[!] Error: {e}")

# --- Phone Lookup ---
def phone_lookup():
    phone = input(Fore.CYAN + "Enter phone (+countrycode...): ").strip()
    if not phone.startswith("+"):
        return
    try:
        url = f"https://api.numlookupapi.com/v1/validate/{phone}"
        proxies = {'http': f'socks5h://127.0.0.1:{TOR_PORT}',
                   'https': f'socks5h://127.0.0.1:{TOR_PORT}'} if is_tor_running() else None
        r = requests.get(url, proxies=proxies, timeout=8)
        save_report("phone_lookup", r.text)
    except Exception as e:
        print(Fore.RED + f"[!] Error: {e}")

# --- Email Breach Lookup ---
def email_breach_lookup():
    email = input(Fore.CYAN + "Enter email: ").strip()
    if "@" not in email:
        return
    try:
        url = f"https://haveibeenpwned.com/unifiedsearch/{email}"
        headers = {"User-Agent": "Mozilla/5.0"}
        proxies = {'http': f'socks5h://127.0.0.1:{TOR_PORT}',
                   'https': f'socks5h://127.0.0.1:{TOR_PORT}'} if is_tor_running() else None
        r = requests.get(url, headers=headers, proxies=proxies, timeout=8)
        save_report("email_breach_lookup", r.text)
    except Exception as e:
        print(Fore.RED + f"[!] Error: {e}")

# --- EXIF Metadata ---
def exif_metadata():
    from PIL import Image
    from PIL.ExifTags import TAGS
    path = input(Fore.CYAN + "Image path: ").strip()
    if not os.path.exists(path):
        return
    try:
        img = Image.open(path)
        exifdata = img._getexif()
        if not exifdata:
            print(Fore.RED + "[!] No EXIF found.")
            return
        exif_text = ""
        for tag_id, value in exifdata.items():
            tag = TAGS.get(tag_id, tag_id)
            exif_text += f"{tag}: {value}\n"
        save_report("exif_metadata", exif_text)
    except Exception as e:
        print(Fore.RED + f"[!] Error: {e}")

# --- Reverse Image Search ---
def reverse_image_search():
    img = input(Fore.CYAN + "Image path: ").strip()
    if not os.path.exists(img):
        return
    save_report("reverse_image_search", f"Search manually: Google Images/Yandex\nFile: {img}")

# --- Face Recognition Search ---
def face_recognition_search():
    print(Fore.RED + "[!] Face++ API key/secret required. Add to code before use.")

# --- Social Media Scraper ---
def social_media_scraper():
    url = input(Fore.CYAN + "Profile URL: ").strip()
    if not url.startswith("http"):
        return
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        proxies = {'http': f'socks5h://127.0.0.1:{TOR_PORT}',
                   'https': f'socks5h://127.0.0.1:{TOR_PORT}'} if is_tor_running() else None
        r = requests.get(url, headers=headers, proxies=proxies, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")
        title = soup.title.string if soup.title else "No title"
        save_report("social_media_scraper", f"URL: {url}\nTitle: {title}")
    except Exception as e:
        print(Fore.RED + f"[!] Error: {e}")

# --- Subdomain Finder ---
def subdomain_finder():
    domain = input(Fore.CYAN + "Domain: ").strip()
    if "." not in domain:
        return
    try:
        url = f"https://crt.sh/?q=%25.{domain}&output=json"
        proxies = {'http': f'socks5h://127.0.0.1:{TOR_PORT}',
                   'https': f'socks5h://127.0.0.1:{TOR_PORT}'} if is_tor_running() else None
        r = requests.get(url, proxies=proxies, timeout=10)
        subs = set([i['name_value'] for i in r.json()])
        save_report("subdomain_finder", "\n".join(subs))
    except Exception as e:
        print(Fore.RED + f"[!] Error: {e}")

# --- Dark Web Leak Search ---
def darkweb_search():
    print(Fore.YELLOW + "[i] Requires Tor and .onion sources configured.")

# --- Google Dork ---
def google_dork():
    query = input(Fore.CYAN + "Enter dork query: ").strip()
    url = f"https://www.google.com/search?q={requests.utils.quote(query)}"
    save_report("google_dork", f"URL: {url}")

# --- Pastebin Leak ---
def pastebin_leak():
    keyword = input(Fore.CYAN + "Keyword: ").strip()
    url = f"https://pastebin.com/search?q={requests.utils.quote(keyword)}"
    save_report("pastebin_leak", f"Search URL: {url}")

# --- Full Recon Mode ---
def full_recon():
    
    username_scanner()1A
    ip_geolocation()
    phone_lookup()
    email_breach_lookup()
    exif_metadata()
    reverse_image_search()
    face_recognition_search()
    social_media_scraper()
    subdomain_finder()
    darkweb_search()
    google_dork()
    pastebin_leak()

# --- Developer Contact ---
def developer_contact():
    print(Fore.CYAN + "\n╔════════════════════════════════════════╗")
    print("║ 📞 Developer Contact                   ║")
    print("╠════════════════════════════════════════╣")
    print("║ 👤 Developer: CYBER ALPHA              ║")
    print("║ 🛠  Team: CYBER GHOST                   ║")
    print("║ ✉️ Email: wait@proton.me     ║")
    print("╚════════════════════════════════════════╝\n")

# --- Menu ---
def main_menu():
    while True:
        try:
            banner(is_tor_running())
            print(Fore.MAGENTA + "\nSelect a module:\n")
            
            print(" 2. 👤  Username Scanner")
            print(" 3. 🌍  IP Geolocation")
            print(" 4. 📞  Phone Lookup")
            print(" 5. ✉️  Email Breach Lookup")
            print(" 6. 🖼  EXIF Metadata Extractor")
            print(" 7. 🔍  Reverse Image Search")
            print(" 8. 😎  Face Recognition Search")
            print(" 9. 🌐  Social Media Scraper")
            print("10. 🕵  Subdomain Finder")
            print("11. 🌑  Dark Web Leak Search")
            print("12. 🛠  Google Dork Automation")
            print("13. 📄  Pastebin Leak Scraper")
            print("14. 🚀  Full Recon Mode")
            print("99. 📞  Developer Contact")
            print(" 0. ❌  Exit\n")
            ch = input(Fore.CYAN + "Enter choice: ").strip()
            elif ch == "2": username_scanner()
            elif ch == "3": ip_geolocation()
            elif ch == "4": phone_lookup()
            elif ch == "5": email_breach_lookup()
            elif ch == "6": exif_metadata()
            elif ch == "7": reverse_image_search()
            elif ch == "8": face_recognition_search()
            elif ch == "9": social_media_scraper()
            elif ch == "10": subdomain_finder()
            elif ch == "11": darkweb_search()
            elif ch == "12": google_dork()
            elif ch == "13": pastebin_leak()
            elif ch == "14": full_recon()
            elif ch == "99": developer_contact()
            elif ch == "0": break
            else:
                print(Fore.RED + "[!] Invalid choice.")
            input(Fore.YELLOW + "\nPress Enter to return to menu...")
        except KeyboardInterrupt:
            print(Fore.RED + "\n[!] Exiting...")
            sys.exit(0)

# --- Entry Point ---
if __name__ == "__main__":
    try:
        tor_ready = start_tor()
        if tor_ready:
            print(Fore.GREEN + "[+] Tor is active.")
        else:
            print(Fore.RED + "[!] Tor not active, using proxy fallback.")
        input(Fore.YELLOW + "Press Enter to continue...")
        main_menu()
    except KeyboardInterrupt:
        print(Fore.RED + "\n[!] Interrupted.")
        sys.exit(0)
