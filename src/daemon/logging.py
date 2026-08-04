import os
from datetime import datetime

from constants import LOG_DIR


def create_log():
    log_file = os.path.join(
        LOG_DIR,
        f"cyphergate_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log",
    )

    with open(log_file, "w", encoding="utf-8") as log:
        log.write(
            f"\n\n===== VPN Session Started: "
            f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} =====\n"
        )

    return log_file
