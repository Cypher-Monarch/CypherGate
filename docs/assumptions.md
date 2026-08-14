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

## IPC assumptions

- The Unix socket filesystem permissions provide the primary local access boundary.
- Clients that can access the socket are trusted to issue privileged commands.
- JSON messages are expected to remain small enough for the current fixed receive buffer.
- The current protocol is request/response oriented and does not provide event subscriptions.

## Configuration assumptions

- VPNGate-provided configurations are untrusted input.
- The GUI writes generated configurations to the user-side VPN directory before requesting a connection.
- The daemon reads the supplied configuration file once, validates the resulting contents, and stages the contents in its daemon-controlled runtime configuration before launching OpenVPN.
- The daemon does not pass the client-supplied configuration path directly to OpenVPN.
- The validator enforces a deliberately restricted OpenVPN feature set.
- `script-security > 0` is unsupported.

## Network assumptions

- VPNGate server metadata contains a base64-encoded OpenVPN configuration.
- DNS AAAA lookup is used as the IPv6 capability check.
- IPv6 is globally disabled through sysctl when the selected server does not appear to support IPv6.

## Future changes

When changing a component, update this document if the change invalidates an assumption.

Architecture decisions should explain both the intended behavior and the reason the behavior is required.
