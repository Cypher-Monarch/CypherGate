# CypherGate

**Autonomous VPN tunneling app. Fetches, patches, connects.**

---

> _“I didn’t know how it worked. I just knew it would.”_

CypherGate is a fully autonomous VPN tunneling app featuring:
- Live VPN server fetching from [VPNGate](https://www.vpngate.net/en/)
- Auto-patches broken OpenVPN configs (fixes cipher issues automagically)
- Modern **Qt GUI** *(with system tray support, notifications, etc.)*
- Minimalist terminal-based legacy TUI (for old-school vibes)
- Auto-connect, manual connect, and fastest-server modes
- Caches server lists for offline use
- Logs every connection for your ~paranoia~ convenience
- Desktop notifications for each step (both GUI & TUI)

Born purely out of spite for broken configs and a desire to automate everything.

---

## ✨ Features
- Automatic VPN server fetching (with fallback to local cache)
- Config patching for modern OpenVPN compatibility  
- Beautiful dark-themed **GUI** with tray controls  
- Minimal, interactive **TUI** for quick terminal use  
- Auto-patches AES ciphers for seamless connections  
- Desktop notifications on connection status  
- Connection logs stored for every session  
- Fully offline-capable after first fetch

---

## ⚙️ Requirements
- Bash
- `curl`
- `base64`
- `whiptail` *(for TUI)*
- `openvpn`
- `notify-send`
- Python 3.x *(bundled with release builds for GUI)*
- `PySide6`, `plyer`, `requests` *(only for source builds)*

---

## 📂 Configuration & Files

All config, cache, and logs are neatly stored under:
```bash
~/.config/cyphergate/
```

## For installation on linux 
```
wget https://github.com/Cypher-Monarch/CypherGate/releases/download/v1.0.1/CypherGate-Linux-v1.0.1.zip
unzip CypherGate-Linux-v1.0.0.zip
cd CypherGate-Linux-v1.0.1
sudo ./install.sh
```
