# Security Model

## Trust boundaries

CypherGate has two major local trust domains:

```text
unprivileged GUI / local client
            │
            │ Unix socket
            ▼
     privileged daemon
            │
            ├── OpenVPN
            ├── log files
            └── system controls
```

The daemon performs operations that require elevated privileges. The GUI communicates with it instead of directly invoking privileged VPN operations.

## Unix socket protection

The daemon creates:

```text
/run/cyphergate/
```

with mode `2750`, owned by root and the `cyphergate` group.

The socket:

```text
/run/cyphergate/cyphergated.sock
```

is created with mode `0660`, also owned by root and the `cyphergate` group. The setgid bit on the runtime directory causes files created within it to inherit the `cyphergate` group.

This replaced the earlier world-accessible `/tmp` socket design.

## OpenVPN configuration policy

The daemon reads the client-supplied configuration file once and validates the resulting contents before launching OpenVPN. It then writes those contents to the daemon-controlled `/run/cyphergate/config.ovpn` and launches OpenVPN against that copy. The client-supplied path is therefore not reopened between validation and use.

This read-once and stage-to-runtime flow prevents a client from replacing the configuration file after validation but before OpenVPN opens it (a time-of-check/time-of-use race).

The validator rejects directives considered capable of executing or loading external behavior, including:

- `up`
- `down`
- `route-up`
- `route-pre-down`
- `ipchange`
- `client-connect`
- `client-disconnect`
- `learn-address`
- `plugin`
- `tls-verify`
- `auth-user-pass-verify`
- `config`

The validator also requires `script-security 0`. Any parsed value greater than zero is rejected.

The validator is intentionally policy-oriented rather than a complete OpenVPN configuration parser.

## Logs

Each VPN session gets a daemon-created log under the configured log directory.

The daemon opens the log for OpenVPN stdout/stderr and keeps the handle in daemon state.

## Security assumptions

The current architecture assumes:

1. membership in the `cyphergate` group is trusted for access to privileged IPC operations;
2. the daemon executable and its runtime directories are protected by the operating system's normal filesystem permissions;
3. OpenVPN is the intended privileged VPN executable;
4. the daemon's configuration-validation policy is sufficient for the supported OpenVPN configuration subset;
5. the daemon's in-memory state is authoritative only while that daemon process is alive.

These assumptions should be revisited as the project gains additional clients and features.
