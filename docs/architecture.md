# CypherGate Architecture

> Current implementation: v2.0.3 (Linux)

## Overview

CypherGate is split into an unprivileged Qt GUI and a privileged daemon.

The GUI is responsible for presentation, server discovery, configuration preparation, and user interaction. The daemon owns the VPN process and the authoritative connection state.

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

`cyphergate.py` creates the Qt application and the `CypherGate` main window.

### Main window

`ui/main_window.py` coordinates the GUI lifecycle and user-facing VPN operations.

It:

- fetches and caches the VPNGate server list;
- filters servers by country;
- prepares `.ovpn` configuration data;
- writes the generated configuration to the user-side VPN directory;
- requests privileged operations through the IPC layer;
- polls daemon state;
- synchronizes widgets from daemon state;
- displays connection/disconnection notifications.

### IPC client

`ipc.py` provides the GUI-side Unix-socket client.

It can:

- start the privileged daemon through `pkexec` when the socket is absent;
- connect to `/run/cyphergate/cyphergated.sock`;
- send JSON commands;
- receive and decode JSON status responses.

### Daemon

`cyphergated.py` owns the Unix socket server and dispatches commands to `daemon.commands`.

The daemon is long-lived and keeps connection state in `daemon.state`. When starting a VPN, it reads the client-supplied configuration once, validates the resulting contents, and stages those contents in the daemon-controlled `/run/cyphergate/config.ovpn` before launching OpenVPN.

### Daemon command layer

`daemon/commands.py` performs privileged operations:

- starting OpenVPN;
- stopping OpenVPN;
- disabling/enabling IPv6;
- returning the current connection state.

### State

`daemon/state.py` contains the daemon's in-memory authoritative state.

The state includes:

- connection status;
- OpenVPN process handle;
- selected country and server metadata;
- configuration path;
- log path and handle;
- connection start time;
- IPv6-disabled state;
- last error;
- monitoring thread/event.

### Connection monitor

`daemon/monitor.py` runs in a daemon thread while a VPN connection is active.

It detects:

- unexpected OpenVPN exit;
- successful OpenVPN initialization by looking for `Initialization Sequence Completed` in the session log.

### Configuration validator

`daemon/validator.py` validates OpenVPN configuration contents before the daemon launches OpenVPN. The daemon reads the client-supplied file once and passes the resulting contents to the validator rather than validating a path and later reopening that path.

It rejects configured dangerous directives and rejects any `script-security` value greater than zero.

### VPN data layer

`vpn/loader.py` parses VPNGate CSV data and applies the local country allowlist.

`vpn/connector.py` prepares a server configuration, adds cipher settings when absent, detects IPv6 support, and writes the resulting configuration file.

## State ownership

The daemon is the source of truth for VPN lifecycle state.

The GUI does not need to keep the VPN process alive. Instead, it asks the daemon for state and maps that state to UI state.

The UI synchronization rules are centralized in `ui/status.py`:

| Daemon state | GUI behavior |
| --- | --- |
| `DISCONNECTED` | Connect/refresh/auto-connect enabled |
| `CONNECTING` | Spinner and cancel state shown |
| `CONNECTED` | Connected country shown; disconnect enabled |
| `ERROR` | Error state shown and connection controls restored |

This separation is what allows a fresh GUI process to reconstruct the state of an already-running daemon connection. If the daemon is already `CONNECTED` when a new GUI instance starts, the GUI can display the existing connection information without waiting for a new connection transition.

## Design intent

The architecture deliberately separates:

1. user interface lifecycle;
2. privileged VPN lifecycle;
3. authoritative connection state;
4. VPN server data processing.

This makes the daemon independently useful to other clients. The current IPC protocol is already sufficient for small external clients such as shell status/uptime/toggle helpers.
