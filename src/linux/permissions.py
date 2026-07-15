import grp
import os

from constants import SOCKET_PATH


def check_permissions():
    groups = {grp.getgrgid(gid).gr_name for gid in os.getgroups()}

    if "cyphergate" not in groups:
        return {
            "ok": False,
            "title": "Setup Required",
            "message": (
                "You are not a member of the 'cyphergate' group.\n\n"
                "Run the following command:\n\n"
                "sudo usermod -aG cyphergate $USER\n\n"
                "Then log out and log back in."
            ),
            "copy": "sudo usermod -aG cyphergate $USER",
        }

    if not os.path.exists(SOCKET_PATH):
        return {
            "ok": False,
            "title": "Daemon Not Running",
            "message": (
                "The CypherGate daemon does not appear to be running.\n\n"
                "Please reinstall CypherGate or restart the daemon."
            ),
            "copy": None,
        }

    return {"ok": True}
