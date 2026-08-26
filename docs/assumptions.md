# Architectural Assumptions

This document records assumptions that are easy to lose during refactors.

## Daemon assumptions

- `cyphergated` is the authoritative owner of the VPN process.
- The daemon is expected to outlive the GUI.
- Daemon connection state is maintained in memory for the lifetime of the daemon process.
- The daemon owns the OpenVPN process; restarting or terminating the daemon therefore terminates the active VPN connection and starts the next daemon instance in a disconnected state.

## GUI assumptions

- The GUI is a client of the daemon rather than the owner of the VPN lifecycle.
- The GUI may disappear while the daemon continues running.
- A new GUI instance must synchronize itself from daemon state.
- GUI polling is currently used for state observation.
- User-facing application behavior is controlled by the per-user settings file where applicable.
- Configuration changes may be applied at runtime for settings explicitly supported by the configuration watcher.

## IPC assumptions

- The Unix socket filesystem permissions provide the primary local access boundary.
- Clients that can access the socket are trusted to issue privileged commands.
- JSON messages are expected to remain small enough for the current fixed receive buffer.
- The current protocol is request/response oriented and does not provide event subscriptions.

## Configuration assumptions

- User configuration is stored in `~/.config/cyphergate/settings.json`.
- Missing configuration values are populated from the application's defaults.
- A configuration value of `null` represents an intentionally unset value where supported by the setting.
- Builtin themes are resolved from the application's bundled theme directory.
- VPNGate-provided configurations are untrusted input.
- The GUI writes generated configurations to the user-side VPN directory before requesting a connection.
- The daemon reads the supplied configuration file once, validates the resulting contents, and stages the contents in its daemon-controlled runtime configuration before launching OpenVPN.
- The daemon does not pass the client-supplied configuration path directly to OpenVPN.
- The validator enforces a deliberately restricted OpenVPN feature set.
- `script-security > 0` is unsupported.

## Server data assumptions

- VPNGate server metadata is provided as CSV data.
- Server rows contain a base64-encoded OpenVPN configuration.
- Server metadata includes country, ping, speed, user count, hostname, IP address, country code, and score.
- The GUI may use server metadata for filtering, sorting, presentation, and connection state.
- The configured default country is matched against the server's long country name.

## Network assumptions

- DNS AAAA lookup is used as the IPv6 capability check.
- IPv6 is globally disabled through sysctl when the selected server does not appear to support IPv6.

## Future changes

When changing a component, update this document if the change invalidates an assumption.

Architecture decisions should explain both the intended behavior and the reason the behavior is required.
