### TEMPORARY UNAVAILABLE 
 
 # cyberghosts-osint
CyberGhosts OSINT – A powerful all-in-one open-source intelligence toolkit with 13+ investigation modules, Tor integration, and full recon mode. Built by CYBER ALPHA for advanced data gathering and analysis.

# 🕵️‍♂️ CyberGhosts OSINT
> **"Hunt the unseen, reveal the hidden."** — An all-in-one OSINT toolkit with 13+ modules, Tor integration, and full recon mode. Developed by **CYBER ALPHA**.

---

## 📌 Features
- 13+ OSINT investigation modules  
- Full Recon Mode (run all modules in sequence)  
- Tor integration with proxy fallback  
- Multi-threaded scanning for speed  
- Save investigation reports in `/reports` folder  
- Cross-platform support (**Termux, Kali, Arch, Windows**)  
- Developer Contact menu option  

---

## 🛠 Modules List  
2. 👤 Username Scanner  
3. 🌍 IP Geolocation  
4. 📞 Phone Lookup  
5. ✉️ Email Breach Lookup  
6. 🖼 EXIF Metadata Extractor  
7. 🔍 Reverse Image Search  
8. 😎 Face Recognition Search  
9. 🌐 Social Media Scraper  
10. 🕵 Subdomain Finder  
11. 🌑 Dark Web Leak Search  
12. 🛠 Google Dork Automation  
13. 📄 Pastebin Leak Scraper  

---

## 📥 Installation

### **Termux**
```bash
pkg update && pkg upgrade -y
pkg install git python tor -y
git clone https://github.com/cyberghosts02/cyberghosts-osint.git
cd cyberghosts-osint
python3 -m venv venv
source venv/bin/activate
python intel_hunter.py
```
### Kali Linux / ParrotOS
```
sudo apt update && sudo apt upgrade -y
sudo apt install git python3 python3-venv tor -y
git clone https://github.com/cyberghosts02/cyberghosts-osint.git
cd cyberghosts-osint
python3 -m venv venv
source venv/bin/activate
python intel_hunter.py
```


### Arch Linux / Manjaro
```
sudo pacman -Syu --noconfirm
sudo pacman -S git python python-virtualenv tor --noconfirm
git clone https://github.com/cyberghosts02/cyberghosts-osint.git
cd cyberghosts-osint
python -m venv venv
source venv/bin/activate
python intel_hunter.py
```


### Windows
```
git clone https://github.com/cyberghosts02/cyberghosts-osint.git
cd cyberghosts-osint
python -m venv venv
venv\Scripts\activate
python intel_hunter.py
```


▶ Usage

Run the tool:
```
python intel_hunter.py
```

*Select a module from the colorful menu or run Full Recon Mode.*


### 📂 Requirements

```
requests
beautifulsoup4
colorama
stem
pillow
```

👤 Developer

CYBER ALPHA – Team CYBER GHOSTS
GitHub: cyberghosts02

*CYBER GHOSTS is a cybersecurity research group led by ALPHA.*
*Specializing in OSINT, penetration testing, and red teaming.*
*Official GitHub: [https://github.com/cyberghosts02]*

**⚠ Disclaimer: This tool is for educational and research purposes only. The developer is not responsible for misuse.**
