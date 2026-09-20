# CypherGate

[![AUR](https://img.shields.io/aur/version/cyphergatevpn-bin?color=gold&label=AUR&logo=arch-linux)](https://aur.archlinux.org/packages/cyphergatevpn-bin)
[![GitHub release](https://img.shields.io/github/v/release/Cypher-Monarch/CypherGate?color=black&logo=github)](https://github.com/Cypher-Monarch/CypherGate/releases)
[![License](https://img.shields.io/github/license/Cypher-Monarch/CypherGate?color=gold)](LICENSE)

---

> "Anyone can hide. Few remain hidden."

CypherGate is a Linux-first VPNGate client designed to make connecting to public VPN servers simple.

VPNGate provides a large collection of public VPN servers, but the raw experience often involves:

- downloading configurations manually
- fixing outdated OpenVPN options
- dealing with inconsistent server data
- troubleshooting connection failures

CypherGate handles the tedious parts.

```
Fetch → Validate → Fix → Connect
```

No config hunting. No manual editing. Just connect.

---

## Showcase

[Showcase.mp4](https://github.com/user-attachments/assets/c10c687c-8eb8-49be-9347-599a60f41e1b)

---

# Features

## Server Management

- Fetch live VPNGate server listings
- Automatically repair incompatible configurations
- Browse and select servers manually
- Connect using the fastest available server
- Cache server data for offline access

## Desktop Experience

- Native Qt6 graphical interface
- System tray integration
- Desktop notifications
- Connection status tracking
- Custom QSS themes
- Configurable settings

## Reliability

CypherGate uses a dedicated backend daemon to manage privileged VPN operations.

```
GUI
|
IPC
|
cyphergated
|
Validation
|
OpenVPN
```

The daemon owns the connection lifecycle, keeping OpenVPN management predictable and preventing stale processes.

---

# Why CypherGate exists

VPNGate is a great resource, but using it manually often feels like maintaining a pile of configuration files.

CypherGate was built around a simple idea:

> Make VPNGate feel like an application instead of a collection of files.

---

# Installation

All official releases since v2.0.1 are cryptographically signed with GnuPG.

## Arch Linux (AUR)

Import the release signing key:

```bash
gpg --keyserver hkps://keys.openpgp.org \
    --recv-keys 9ED87F6065033606670941AAC6C9B498797C980E
```

Install:

```bash
yay -S cyphergatevpn-bin
```

---

## Linux

Download and run the installer:

```bash
curl -fsSL https://github.com/Cypher-Monarch/CypherGate/releases/latest/download/install.sh > install.sh
sudo bash install.sh
```

---

# Usage

Launch CypherGate from your application menu:

```
CypherGate VPN
```

The GUI handles:

* server selection
* connection management
* settings
* themes
* status monitoring

---

# Architecture

CypherGate separates user interaction from privileged operations.

The application communicates with `cyphergated` through IPC.

Responsibilities are separated:

| Component   | Responsibility       |
| ----------- | -------------------- |
| GUI         | User interaction     |
| IPC         | Communication layer  |
| cyphergated | Connection lifecycle |
| Validator   | Configuration checks |
| OpenVPN     | VPN tunnel           |

This design keeps the backend small, controlled, and easier to audit.

---

# Configuration

User configuration:

```bash
~/.config/cyphergate/
```

Logs:

```bash
/var/log/cyphergate
```

---

# Customization

CypherGate supports customisation through QSS themes and configuration files.

Documentation:

* [Settings](docs/settings.md)
* [Theming](docs/theming.md)
* [Theme Showcase](showcase.md)

---

# Documentation

Technical documentation is available in [CypherDocs](https://cypher-monarch.github.io/CypherDocs/cyphergate/docs/)

Includes:

* Architecture overview
* IPC protocol
* Security model
* Configuration system
* Codebase documentation
* Assumptions and design decisions

---

# Development

CypherGate is built with:

* Python
* Qt6
* OpenVPN
* systemd
* JSON-based IPC

The project follows a modular design philosophy:

* small components
* explicit responsibilities
* documented behaviour

---

# Contributing

Contributions are welcome.

Before submitting changes:

1. Read the documentation
2. Check existing issues
3. Keep changes focused
4. Document architectural decisions where relevant

See:

* [CONTRIBUTING.md](CONTRIBUTING.md)
* [SECURITY.md](SECURITY.md)

---

# Security

CypherGate takes connection management seriously.

The daemon:

* validates configurations before execution
* limits what operations can be performed
* manages OpenVPN lifecycle explicitly
* avoids leaving unmanaged processes behind

Security concerns should be reported through:

[SECURITY.md](SECURITY.md)

---

# License

CypherGate is licensed under the GNU General Public License v3.0.

See [LICENSE](LICENSE) for details.

---

> It looks how it should.
> It works how it should.
> The "should" is yours.
