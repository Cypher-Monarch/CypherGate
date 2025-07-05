# CypherGate

**Autonomous VPN tunneling script. Fetches, patches, connects.**

---

> _“I didn’t know how it worked. I just knew it would.”_

CypherGate is a Bash-powered VPN tunneling script that:
- Fetches live VPN server lists from [VPNGate](https://www.vpngate.net/en/)
- Auto-patches broken OpenVPN configs (fixes cipher issues automagically)
- Lets you select servers via a terminal-based UI (whiptail)
- Connects automatically through OpenVPN
- Caches server lists for offline use
- Logs everything for your ~paranoia~ convenience
- Sends desktop notifications for each step

Born purely out of spite for broken configs and a desire to automate everything.

---

## ✨ Features
- Automatic VPN server fetching (with fallback to local cache)
- Config patching for modern OpenVPN compatibility  
- Simple, interactive server selection menu  
- Auto-patches AES ciphers to prevent connection issues  
- Desktop notifications via `notify-send`
- Connection logs stored for every session  
- Fully offline-capable after first fetch

---

## ⚙️ Requirements
- Bash
- `curl`
- `base64`
- `whiptail`
- `openvpn`
- `notify-send`

---

## 📂 Configuration & Files

All config, cache, and logs are neatly stored under:
```bash
~/.config/cyphergate/
```
