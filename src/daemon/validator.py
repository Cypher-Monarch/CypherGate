FORBIDDEN_DIRECTIVES = frozenset(
    {
        "up",
        "down",
        "route-up",
        "route-pre-down",
        "ipchange",
        "client-connect",
        "client-disconnect",
        "learn-address",
        "plugin",
        "tls-verify",
        "auth-user-pass-verify",
    }
)


def validate_config(config_path):
    script_security = 0

    with open(config_path, encoding="utf-8") as config:
        for line in config:
            line = line.strip()

            if not line or line.startswith(("#", ";")):
                continue

            tokens = line.split()
            directive = tokens[0].lower()

            if directive == "script-security":
                if len(tokens) >= 2:
                    try:
                        script_security = int(tokens[1])
                    except ValueError:
                        raise ValueError("Invalid script-security directive.")

                continue

            if directive in FORBIDDEN_DIRECTIVES:
                raise ValueError(f"Forbidden OpenVPN directive: {directive}")

    if script_security > 0:
        raise ValueError("OpenVPN configurations must use 'script-security 0'.")
