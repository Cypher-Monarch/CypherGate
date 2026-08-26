# Codebase Guide

## Repository layout

```text
src
├── config
│   ├── defaults.py
│   ├── fallback_theme.py
│   ├── manager.py
│   ├── theme.py
│   └── watcher.py
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
├── requirements.txt
└── update.py
```

## Execution flow

### GUI startup

1. `cyphergate.py` creates `QApplication`.
2. `CypherGate` initializes the window.
3. Configuration is loaded and validated.
4. Widgets, layout, signals, tray icon, and update checking are configured.
5. The GUI checks local permissions.
6. The GUI asynchronously ensures that the daemon socket is available.
7. The VPNGate server list is fetched; the local cache is used if the request fails.
8. Server data is parsed and displayed according to the configured table layout.
9. Current daemon state is queried and applied to the UI.

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

The GUI sees the state transition, synchronizes its widgets, and shows connection information including the country, server IP, ping, speed, and users. If a new GUI instance starts while the daemon is already `CONNECTED`, it can show the same connection information from the existing daemon state.

### Disconnecting

The GUI sends `STOP_VPN` and then `ENABLE_IPV6`.

The daemon terminates OpenVPN, removes `/run/cyphergate/config.ovpn`, closes the log handle, stops the monitor, and resets connection state.

## Server data

The application consumes the VPNGate iPhone API URL configured in `constants.py`.

Server rows are parsed from CSV. The relevant fields are converted into:

```text
(
    country,
    ping,
    speed,
    users,
    hostname,
    ip,
    country_short,
    score,
    config_base64,
)
```

The server metadata is retained independently of the table presentation. The table configuration determines which fields are displayed and their order.

Servers can be filtered by country and sorted using a configurable field and sort order. Values such as ping and speed are parsed specially so that missing or non-numeric values can be sorted safely.

The optional country allowlist is read from `countries.conf`.

## Configuration

Application settings are stored in:

```text
~/.config/cyphergate/settings.json
```

The configuration is divided into several sections:

* `theme`: builtin or custom theme selection;
* `icons`: icon sizes and colors;
* `widgets`: widget-specific settings such as spinner appearance and animation;
* `application`: application behavior such as tray minimization, notifications, and status polling;
* `vpn`: connection timeout and default country;
* `table`: displayed server columns and sorting configuration.

`config/manager.py` loads settings, merges missing values from the defaults, validates their types, and writes the resulting configuration when necessary.

`config/theme.py` resolves builtin and custom theme paths and loads the selected stylesheet.

`config/watcher.py` monitors the settings file and the currently selected theme file. Changes to configuration are applied without restarting the application where supported.

### Hot-reloadable settings

Configuration changes can update:

* application icons and their sizes/colors;
* system tray action icons;
* spinner size, color, thickness, FPS, and rotation speed;
* the active theme;
* server table columns;
* server table sorting.

Settings that affect application lifecycle or VPN behavior are applied according to their respective runtime usage rather than being treated as generic UI hot-reload properties.

## Configuration preparation

`vpn.connector.prepare_connection()`:

* decodes the server's base64 OpenVPN configuration;
* adds `data-ciphers` when absent;
* adds `cipher` when absent;
* extracts the remote host;
* checks for an AAAA record;
* adds IPv6-related directives when the server supports IPv6;
* otherwise asks the caller to disable IPv6.

The prepared configuration is written to the configured VPN directory.

## UI responsibilities

The UI modules are deliberately small:

* `widgets.py`: widget creation and signal wiring;
* `layout.py`: widget arrangement;
* `window.py`: window styling;
* `status.py`: state-to-widget mapping;
* `tray.py`: system tray integration;
* `animations.py`: visual transitions;
* `events.py`: window interaction events;
* `icons.py`: SVG icon rendering/cache and icon application;
* `spinner.py`: connection spinner and spinner configuration.

The `config` package owns settings loading, defaults, theme resolution, and configuration watching.

The main application class remains the coordinator for VPN workflows rather than putting all implementation details into one file.
