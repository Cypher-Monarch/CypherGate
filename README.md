# CypherGate

[![AUR](https://img.shields.io/aur/version/cyphergatevpn-bin?color=gold&label=AUR&logo=arch-linux)](https://aur.archlinux.org/packages/cyphergatevpn-bin)
[![GitHub release](https://img.shields.io/github/v/release/Cypher-Monarch/CypherGate?color=black&logo=github)](https://github.com/Cypher-Monarch/CypherGate/releases)
[![License](https://img.shields.io/github/license/Cypher-Monarch/CypherGate?color=gold)](LICENSE)

---

## CypherGate

> _“Anyone can hide. Few remain hidden.”_

I made this because VPNGate configs are… let’s just say
**not exactly plug-and-play**

CypherGate:

- fetches servers
- fixes their broken configs
- connects without asking you to debug nonsense

So yeah:

> click → connect → done

---

## 🎬 Showcase

[Showcase.mp4](https://github.com/user-attachments/assets/5f362c0a-4c95-4375-a177-99b25eb1fc27)

---

## ⚡ What it does (without the marketing talk)

- grabs live VPNGate servers
- auto-fixes configs that shouldn’t have been broken in the first place
- runs a gold-on-black Qt GUI (yes it’s opinionated, no I won’t apologize)
- also has a TUI if you live in the terminal
- lets you:
  - auto-connect
  - pick manually
  - or just go “fastest server pls”

- caches servers so you’re not stuck when offline
- logs everything (for your ~paranoia~ curiosity)
- sends notifications so you know what’s going on

---

## 🧠 Why this exists

Because I got tired of:

- broken configs
- outdated ciphers
- “just edit this file manually bro”

So I made something that:

> just handles it

---

## ⚙️ Requirements (TUI only)

- `bash`
- `curl`
- `base64`
- `whiptail`
- `openvpn`
- `notify-send`

---

## 📂 Where stuff goes

```bash
~/.config/cyphergate/
```

Logs:

- Linux → `~/.config/cyphergate/logs`
- Windows → `%USERPROFILE%\.config\cyphergate\logs`

---

## 📦 Installation (All official releases since v2.0.1 are cryptographically signed with GnuPG)

### AUR

1. **FIRST TIME ONLY** - Import CypherGate release signing keys with:

```bash
gpg --keyserver hkps://keys.openpgp.org \
    --recv-keys 9ED87F6065033606670941AAC6C9B498797C980E
```

2. Use your favourite AUR helper to install `cyphergatevpn-bin`!

```bash
yay -S cyphergatevpn-bin
```

---

### Linux (general)

```bash
curl -fsSL https://github.com/Cypher-Monarch/CypherGate/releases/latest/download/install.sh > install.sh
sudo bash install.sh
```

---

### Windows (For the "Where is my .exe?" people)

- Installer → [Here you go](https://github.com/Cypher-Monarch/CypherGate/releases/download/v1.0.1/CypherGateInstaller-v1.0.1.exe)
- Portable → [There you go](https://github.com/Cypher-Monarch/CypherGate/releases/download/v1.0.1/CypherGate-Windows-v1.0.1.zip)

#### AS OF v1.0.1 Development of the windows version is discontinued

---

## 🖥️ Usage

- Linux GUI → launch **CypherGate VPN**
- Linux TUI → `cyphergate.sh`
- Windows → Start Menu / `CypherGate.exe`

---

## 🎨 Customization

Want to make CypherGate look and behave the way you want?

- [Settings](docs/settings.md) — Configure application behaviour and server tables
- [Theming](docs/theming.md) — Create custom QSS themes
- [Theme Showcase](showcase.md) — Browse the builtin themes and see how to use them

---

## ⚡ Final note

> **It looks how it should. It works how it should. The 'should' is yours**

---

## License

CypherGate is licensed under the GNU General Public License v3.0 (GPL-3.0).
See the [LICENSE](https://github.com/Cypher-Monarch/CypherGate/blob/main/LICENSE) file for details.
