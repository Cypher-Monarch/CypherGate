# Contributing to CypherGate

Thanks for contributing.

## Before making changes

Read:

- `docs/architecture.md`
- `docs/codebase.md`
- `docs/ipc.md`
- `docs/security-model.md`
- `docs/assumptions.md`

CypherGate has a privileged daemon boundary. Changes touching the daemon, IPC, OpenVPN configuration handling, filesystem paths, or system controls deserve additional review.

## Development principles

### Keep privilege boundaries explicit

Prefer:

```text
GUI → IPC → daemon → privileged operation
```

over adding privileged behavior directly to the GUI.

### Keep daemon state authoritative

If a new feature needs connection state, consider whether that state belongs in `daemon/state.py` rather than being maintained only by the GUI.

### Validate untrusted input

Treat VPN server data, configuration files, IPC requests, filesystem paths, and network responses as untrusted unless an explicit trust assumption says otherwise.

### Preserve lifecycle independence

The daemon should remain capable of owning an active VPN connection independently of the GUI process.

## IPC changes

When adding or changing an IPC command:

1. document the command in `docs/ipc.md`;
2. document its request and response shape;
3. document privilege implications;
4. update clients that depend on it;
5. consider backward compatibility.

## Security-sensitive changes

Changes involving:

- OpenVPN configuration validation;
- filesystem paths;
- Unix socket permissions;
- process spawning;
- root privileges;
- sysctl;
- log creation;
- IPC authorization

should include tests or a clear explanation of why the behavior is safe.

Do not describe an intended security property as implemented until the code actually enforces it.

## Pull requests

A useful PR description should explain:

- what changed;
- why it changed;
- architectural impact;
- security impact;
- testing performed;
- any known limitations.

Keep unrelated refactors out of security fixes when practical. Small, reviewable changes are easier to audit.

## Commit messages

Use concise conventional-style commit messages where practical, for example:

```text
fix(daemon): reject unsafe OpenVPN directives
refactor(ipc): centralize daemon status requests
docs(security): document configuration trust boundary
```
