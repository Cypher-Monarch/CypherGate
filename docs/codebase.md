# Codebase Guide

## Repository layout

```text
src
├── daemon
│   ├── commands.py
│   ├── logging.py
│   ├── monitor.py
│   ├── setup.py
│   ├── state.py
│   └── validator.py
├── ui
│   ├── animations.py
│   ├── events.py
│   ├── icons.py
│   ├── layout.py
│   ├── main_window.py
│   ├── spinner.py
│   ├── status.py
│   ├── tray.py
│   ├── widgets.py
│   └── window.py
├── vpn
│   ├── connector.py
│   └── loader.py
├── constants.py
├── cyphergated.py
├── cyphergate.py
├── ipc.py
├── permissions.py
└── update.py
```

## Execution flow

### GUI startup

1. `cyphergate.py` creates `QApplication`.
2. `CypherGate` initializes the window.
3. Widgets, layout, signals, tray icon, and update checking are configured.
4. The GUI checks local permissions.
5. The GUI asynchronously ensures that the daemon socket is available.
6. The VPNGate server list is fetched; the local cache is used if the request fails.
7. Server data is parsed and displayed.
8. Current daemon state is queried and applied to the UI.

### Connecting

The GUI:

1. gets the selected server;
2. prepares the OpenVPN configuration;
3. checks whether the endpoint supports IPv6;
4. disables IPv6 through the daemon when necessary;
5. writes the generated `.ovpn` file;
6. sends `START_VPN` with the configuration path and server metadata;
7. polls daemon status until the connection reaches a terminal state.

The daemon:

1. reads the supplied configuration file once;
2. validates the resulting configuration contents;
3. writes the validated contents to `/run/cyphergate/config.ovpn`;
4. creates a session log;
5. records connection metadata in global state;
6. starts `/usr/bin/openvpn --config /run/cyphergate/config.ovpn`;
7. starts the connection monitor.
### Successful connection

The monitor looks for OpenVPN's `Initialization Sequence Completed` marker in the session log. Once found, daemon state becomes `CONNECTED`.

The GUI sees the state transition, synchronizes its widgets, and shows connection information including the country, server metadata, and current public IPv4. If a new GUI instance starts while the daemon is already `CONNECTED`, it can show the same connection information from the existing daemon state.

### Disconnecting

The GUI sends `STOP_VPN` and then `ENABLE_IPV6`.

The daemon terminates OpenVPN, removes `/run/cyphergate/config.ovpn`, closes the log handle, stops the monitor, and resets connection state.

## Server data

The application consumes the VPNGate iPhone API URL configured in `constants.py`.

Server rows are parsed from CSV. The relevant fields are converted into:

```text
(country, ping, speed, users, config_base64)
```

The optional country allowlist is read from `countries.conf`.

## Configuration preparation

`vpn.connector.prepare_connection()`:

- decodes the server's base64 OpenVPN configuration;
- adds `data-ciphers` when absent;
- adds `cipher` when absent;
- extracts the remote host;
- checks for an AAAA record;
- adds IPv6-related directives when the server supports IPv6;
- otherwise asks the caller to disable IPv6.

The prepared configuration is written to the configured VPN directory.

## UI responsibilities

The UI modules are deliberately small:

- `widgets.py`: widget creation and signal wiring;
- `layout.py`: widget arrangement;
- `window.py`: window styling;
- `status.py`: state-to-widget mapping;
- `tray.py`: system tray integration;
- `animations.py`: visual transitions;
- `events.py`: window interaction events;
- `icons.py`: SVG icon rendering/cache;
- `spinner.py`: connection spinner.

The main application class remains the coordinator for VPN workflows rather than putting all implementation details into one file.
