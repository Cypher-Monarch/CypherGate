# CypherGate


[![AUR](https://img.shields.io/aur/version/cyphergatevpn-bin?color=gold&label=AUR&logo=arch-linux)](https://aur.archlinux.org/packages/cyphergatevpn-bin)  [![GitHub release](https://img.shields.io/github/v/release/Cypher-Monarch/CypherGate?color=black&logo=github)](https://github.com/Cypher-Monarch/CypherGate/releases)  [![License](https://img.shields.io/github/license/Cypher-Monarch/CypherGate?color=gold)](LICENSE)  


**CypherGate — an autonomous VPN tunneling client. Fetch. Patch. Connect.**  

---

> _“Anyone can hide. Few remain hidden.”_  

CypherGate takes the pain out of VPNGate. It fetches live OpenVPN servers, auto-repairs their broken configs, and connects you in seconds.  
No manual fixes, no fiddling — just click, connect, and tunnel.  

What you get out of the box:  
- 🌐 Live VPN server fetching from [VPNGate](https://www.vpngate.net/en/)  
- 🛠️ Auto-patching of broken configs (ciphers fixed automatically)  
- 🎨 Sleek gold-on-black **Qt GUI** with tray support & notifications  
- 🖥️ Minimalist legacy **TUI** for terminal enjoyers  
- 🚀 Auto-connect, manual select, or fastest-server mode  
- 📦 Server cache for offline use  
- 📝 Per-session connection logs (for your ~paranoia~ convenience)  
- 🔔 Desktop notifications at every step  

Born out of frustration with half-working configs — refined into something smooth and automatic.  

---

## ✨ Features  
- 🌐 Live server fetching (with offline cache fallback)  
- 🛠️ Smart config patching for modern OpenVPN compatibility  
- 🎨 Dark-themed GUI with animations and tray controls  
- 🖥️ Simple TUI for quick, no-nonsense terminal use  
- 🔑 Auto-injected AES/ChaCha20 ciphers  
- 🔔 Real-time notifications on connect/disconnect  
- 📝 Session logs saved automatically  
- 📴 Fully functional even offline after first fetch  


---

## ⚙️ Requirements (TUI only): 
- `Bash`
- `curl`
- `base64`
- `whiptail` *(for TUI)*
- `openvpn`
- `notify-send`
---

## 📂 Configuration & Files:

All config, cache, and logs are neatly stored under:
```
~/.config/cyphergate/
```

## For installation on ARCH based Distros:
```
yay -S cyphergatevpn-bin
```

## For installation on LINUX (general):

```
curl -L -o install.sh https://raw.githubusercontent.com/Cypher-Monarch/CypherGate/main/CORE/LINUX/QT_GUI/install.sh
chmod +x install.sh
sudo ./install.sh
```

## 🪟 Windows:

`Grab the latest release`

- `CypherGateInstaller.exe` → Easy setup
- `CypherGate.zip` → Portable build

## 🖥️ Usage:

- Linux GUI → run CypherGate VPN
- Linux Legacy TUI → run cyphergate.sh
- Windows → launch from Start Menu or run CypherGate.exe

## Logs are stored under:

- Linux → `~/.config/cyphergate/logs`
- Windows → `%USERPROFILE%\.config\cyphergate\logs`

