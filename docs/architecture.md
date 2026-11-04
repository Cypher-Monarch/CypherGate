# CypherGate Architecture

> Current implementation: v2.1.2 (Linux)

## Overview

CypherGate is split into an unprivileged Qt GUI and a privileged daemon.

The GUI is responsible for presentation, server discovery, configuration management, VPN configuration preparation, diagnostics collection, and user interaction. The daemon owns the VPN process, privileged system operations, and authoritative connection state.

```text
                    ┌─────────────────────┐
                    │   CypherGate GUI    │
                    │     (PySide6)       │
                    └──────────┬──────────┘
                               │ Unix socket / JSON
                               ▼
                    ┌─────────────────────┐
                    │    cyphergated      │
                    │  privileged daemon  │
                    └──────────┬──────────┘
                               │
                    ┌──────────┴──────────┐
                    ▼                     ▼
               OpenVPN process       system controls
                                      (IPv6 sysctl)
```

The daemon is intentionally persistent relative to the GUI. A GUI restart does not inherently terminate an existing VPN process; a newly launched GUI can query daemon state and synchronize its UI from that state.

## Components

### GUI entry point

`cyphergate.py` creates the Qt application, configures the application icon, instantiates the `CypherGate` main window, and starts the Qt event loop.

### Main window

`ui/main_window.py` coordinates the GUI lifecycle and user-facing VPN operations.

It:

- fetches and caches the VPNGate server list;
- filters servers by country;
- sorts servers according to the configured table settings;
- prepares `.ovpn` configuration data;
- writes the generated configuration to the user-side VPN directory;
- requests privileged operations through the IPC layer;
- continuously polls daemon state;
- synchronizes widgets and system-tray state from daemon state;
- applies user configuration to the GUI;
- coordinates dashboard and logs-page navigation;
- collects and formats diagnostic information;
- displays connection/disconnection notifications.

### User interface

The `ui/` package contains the application interface and its supporting components.

`ui/layout.py` assembles the main application pages and their layout.

`ui/dashboard.py` constructs and updates the connected-state dashboard. It presents connection information, session metrics, and user-facing actions such as copying diagnostics, opening logs, and disconnecting.

`ui/log_page.py` constructs the connection-log viewer. The viewer displays the active session log reported by the daemon.

`ui/status.py` synchronizes the GUI with daemon connection state.

Other UI modules provide widget creation, event handling, animations, icons, fonts, system-tray integration, window configuration, and the connection spinner.

### Configuration

The `config/` package manages application configuration and theme selection.

It:

- loads and validates `settings.json`;
- merges missing configuration values from the defaults;
- resolves builtin and custom themes;
- provides a fallback stylesheet;
- watches the settings and active theme files for changes.

Configuration is stored per-user under `~/.config/cyphergate/settings.json`.

Settings cover theme selection, icon appearance, spinner behavior, application behavior, VPN defaults, and server-table presentation.

### IPC client

`ipc.py` provides the GUI-side Unix-socket client.

It can:

- start the privileged daemon through `pkexec` when required;
- connect to `/run/cyphergate/cyphergated.sock`;
- send JSON commands;
- receive and decode JSON status responses.

The GUI uses this interface for privileged operations and retrieving daemon state.

### Daemon

`cyphergated.py` owns the Unix socket server and dispatches incoming commands to `daemon.commands`.

The daemon is long-lived and keeps connection state in `daemon.state`.

When starting a VPN, it reads the client-supplied configuration, validates the resulting contents, and stages those contents in the daemon-controlled `/run/cyphergate/config.ovpn` before launching OpenVPN.

### Daemon command layer

`daemon/commands.py` performs privileged operations:

- starting OpenVPN;
- stopping OpenVPN;
- disabling or enabling IPv6;
- returning the current connection state.

When a connection starts, the daemon creates a timestamped session log and redirects OpenVPN output into it.

### State

`daemon/state.py` contains the daemon's in-memory authoritative state.

The state includes:

- connection status;
- OpenVPN process handle;
- selected country;
- selected server metadata, including country code, hostname, IP, score, ping, speed, and user count;
- configuration path;
- active log path and handle;
- connection start time;
- IPv6-disabled state;
- last error;
- monitoring thread and stop event.

When a connection is stopped, the daemon resets its connection state, including the active log path.

### Connection monitor

`daemon/monitor.py` runs in a daemon thread while a VPN connection is active.

It detects:

- unexpected OpenVPN exit;
- successful OpenVPN initialization by looking for `Initialization Sequence Completed` in the session log.

### Configuration validator

`daemon/validator.py` validates OpenVPN configuration contents before the daemon launches OpenVPN.

The daemon reads the client-supplied file once and passes the resulting contents to the validator rather than validating a path and later reopening that path.

The validator rejects configured dangerous directives and rejects any `script-security` value greater than zero.

### VPN data layer

`vpn/loader.py` parses VPNGate CSV data and applies the local country allowlist. It retains server metadata used for filtering, sorting, table presentation, and connection state.

`vpn/connector.py` prepares a server configuration, adds cipher settings when absent, detects IPv6 support, and writes the resulting configuration file.

### Diagnostics

`diagnostics.py` collects and formats application diagnostic information.

The diagnostic report includes:

- CypherGate version;
- Python, PySide6, and Qt versions;
- distribution and system architecture;
- configuration availability;
- selected theme;
- daemon availability;
- coarse VPN connection state.

The collector uses explicitly approved fields. It does not collect server metadata, configuration contents, file paths, or raw logs.

The main window coordinates collection using the current settings and latest daemon status, then provides the formatted report through the clipboard.

### Log reader

`log_reader.py` provides the GUI-side log-reading function.

It accepts a file path and returns the file contents. It has no responsibility for discovering log files, managing session state, or communicating with the daemon.

The main window obtains the active session log path from the daemon's status response and passes it to the reader. The logs page displays the resulting contents.

## State ownership

The daemon is the source of truth for VPN lifecycle state.

The GUI does not need to keep the VPN process alive. Instead, it asks the daemon for state and maps that state to UI state.

The GUI continuously polls daemon state so that each GUI instance remains synchronized with the authoritative daemon state, including system-tray state.

The UI synchronization rules are centralized in `ui/status.py`:

| Daemon state | GUI behavior |
| --- | --- |
| `DISCONNECTED` | Connect, refresh, and auto-connect controls enabled |
| `CONNECTING` | Spinner and cancel state shown |
| `CONNECTED` | Connected dashboard shown; disconnect enabled |
| `ERROR` | Error state shown and connection controls restored |

This separation allows a fresh GUI process to reconstruct the state of an already-running daemon connection. If the daemon is already `CONNECTED` when a new GUI instance starts, the GUI can display the existing connection information without waiting for a new connection transition.

The connected dashboard is a presentation of daemon-reported state, not an independent connection-state manager.

The logs viewer follows the same ownership model: the daemon reports the active session log path, and the GUI reads that file directly. The GUI does not maintain a separate authoritative copy of the session's log lifecycle.

## Design intent

The architecture deliberately separates:

1. user interface lifecycle and presentation;
2. privileged VPN lifecycle;
3. authoritative connection state;
4. VPN server data processing;
5. user configuration and presentation preferences;
6. application diagnostics and log presentation.

The GUI remains responsible for presentation and configuration while the daemon remains responsible for privileged VPN lifecycle and authoritative state.

This keeps the privileged daemon independent of the GUI's presentation choices. The current IPC protocol is sufficient for the GUI and small external clients such as shell status, uptime, and toggle helpers.
