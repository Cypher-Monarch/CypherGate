import csv
import os

from constants import COUNTRIES_CONF, TABLE_COLUMNS


def load_allowed_countries():
    if os.path.exists(COUNTRIES_CONF):
        with open(COUNTRIES_CONF, "r", encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip()]
    return None


def parse_server_data(data):
    lines = data.splitlines()[2:]
    reader = csv.reader(lines)

    servers = []
    countries = set()

    allowed_countries = load_allowed_countries()

    for row in reader:
        if len(row) < 15:
            continue

        country = row[5]

        if allowed_countries and country not in allowed_countries:
            continue

        hostname = row[0]
        ip = row[1]
        score = row[2]
        ping = row[3] + " ms"
        speed = str(int(int(row[4]) / 1000)) + " kbps"
        country = row[5]
        country_short = row[6]
        users = row[9]
        config_b64 = row[-1]

        servers.append(
            (
                country,
                ping,
                speed,
                users,
                hostname,
                ip,
                country_short,
                score,
                config_b64,
            )
        )
        countries.add(country)

    return servers, sorted(countries)


def filter_servers(servers, country, settings):
    filtered = [s for s in servers if s[0] == country]

    sort_by = settings["table"]["sort_by"]
    sort_order = settings["table"]["sort_order"]
    index = TABLE_COLUMNS[sort_by][1]

    def key(server):
        value = server[index]

        if sort_by in ("ping", "speed"):
            return int(value.split()[0])

        return float(value)

    valid = []
    invalid = []

    for server in filtered:
        try:
            if server[index] == "-":
                invalid.append(server)
            else:
                key(server)
                valid.append(server)
        except (ValueError, TypeError):
            invalid.append(server)

    valid.sort(
        key=key,
        reverse=sort_order == "descending",
    )

    return valid + invalid
