# IPC API

## Transport

CypherGate uses a Unix domain stream socket:

```text
/run/cyphergate/cyphergated.sock
```

The daemon creates the containing directory with mode `2750` and the socket with mode `0660`. The `cyphergate` group is used for access control.

The client sends a single JSON object per connection.

Current client-side requests are shaped as:

```json
{"action": "STATUS"}
```

or:

```json
{
  "action": "START_VPN",
  "config": "/path/to/server.ovpn",
  "country": "Japan",
  "ping": "42 ms",
  "speed": "100000 kbps",
  "users": "123"
}
```

## Actions

### `STATUS`

Returns a JSON object containing the daemon's current state.

Example shape:

```json
{
  "status": "CONNECTED",
  "country": "Japan",
  "ping": "42 ms",
  "speed": "100000 kbps",
  "users": "123",
  "config": "/run/cyphergate/config.ovpn",
  "log_file": "/var/log/cyphergate/cyphergate_....log",
  "started_at": 1750000000.0,
  "ipv6_disabled": false,
  "last_error": null
}
```

_The exact values are runtime-dependent._

### `START_VPN`

Requests that the daemon start an OpenVPN process using the supplied configuration.

The `config` field is the path to the client-provided OpenVPN configuration. The daemon reads that file once, validates the resulting contents, and writes the validated contents to the daemon-controlled `/run/cyphergate/config.ovpn`. OpenVPN is then launched using that runtime copy rather than reopening the client-supplied path.

The request may include:

- `config`
- `country`
- `ping`
- `speed`
- `users`

The daemon stores the connection metadata in its in-memory state. The active `config` value reported by `STATUS` refers to the daemon-controlled runtime configuration.

### `STOP_VPN`

Terminates the current OpenVPN process, removes the daemon-controlled runtime configuration, closes its log, stops monitoring, and resets connection state.

### `DISABLE_IPV6`

Runs the system IPv6 disable sysctl and records `ipv6_disabled = true`.

### `ENABLE_IPV6`

Runs the corresponding sysctl to re-enable IPv6 and records `ipv6_disabled = false`.

## Authorization model

IPC access is controlled at the filesystem level by ownership and mode of the Unix socket and its parent directory.

The daemon currently does not implement a separate application-level authentication or authorization protocol inside the JSON messages.

Therefore, membership/access to the `cyphergate` group is part of the trusted boundary.

## Protocol limitations

The current daemon accepts JSON from a connected client and dispatches directly on `action`.

There is currently no documented protocol version field, request ID, subscription mechanism, or structured error response.

These are potential future API improvements and should be treated as compatibility work before external clients depend heavily on the protocol.
