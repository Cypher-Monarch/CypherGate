# Security Policy

## Supported versions

Security fixes should target the latest released version of CypherGate.

For the current release, see the project's release information.

## Reporting a vulnerability

Please do **not** publicly disclose an unpatched security vulnerability in an issue or discussion.

Report security issues privately through the repository's configured private security reporting mechanism. Include:

- affected version;
- affected component/file if known;
- clear description of the issue;
- reproduction steps or proof of concept when safe to provide;
- impact assessment;
- suggested mitigation, if known.

If the issue involves the privileged daemon, explicitly state whether exploitation requires membership in the `cyphergate` group or another local privilege.

## Security architecture

CypherGate uses a privileged daemon for VPN operations. The GUI communicates with the daemon over a Unix socket protected by filesystem ownership and permissions.

The daemon reads client-supplied OpenVPN configuration files once, validates the resulting contents, and stages the validated configuration under `/run/cyphergate` before launching OpenVPN. It rejects a defined set of dangerous directives as well as `script-security` values greater than zero. This prevents the validated path from being replaced before OpenVPN uses it.

See `docs/security-model.md` for the current security assumptions and known limitations.

## Disclosure

Security fixes should be accompanied by a clear changelog entry describing the impact and the affected versions without unnecessarily publishing exploit details before users have had an opportunity to update.
