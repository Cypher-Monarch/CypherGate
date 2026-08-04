import grp
import os
import socket
import stat

from constants import LOG_DIR, SOCKET_DIR, SOCKET_PATH


def create_server():
    gid = grp.getgrnam("cyphergate").gr_gid

    os.makedirs(LOG_DIR, mode=0o750, exist_ok=True)
    os.chown(LOG_DIR, 0, gid)
    os.chmod(LOG_DIR, 0o750)

    os.makedirs(SOCKET_DIR, mode=0o750, exist_ok=True)
    os.chown(SOCKET_DIR, 0, gid)
    os.chmod(SOCKET_DIR, 0o750)

    if os.path.exists(SOCKET_PATH):
        if stat.S_ISSOCK(os.stat(SOCKET_PATH).st_mode):
            os.unlink(SOCKET_PATH)
        else:
            raise RuntimeError(f"{SOCKET_PATH} exists but is not a socket")

    server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    server.bind(SOCKET_PATH)

    os.chown(SOCKET_PATH, 0, gid)
    os.chmod(SOCKET_PATH, 0o660)

    server.listen(5)

    return server
