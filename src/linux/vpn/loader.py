import csv
import os

from constants import COUNTRIES_CONF


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

        ping = row[3] + " ms"
        speed = str(int(int(row[4]) / 1000)) + " kbps"
        users = row[2]
        config_b64 = row[-1]

        servers.append((country, ping, speed, users, config_b64))
        countries.add(country)

    return servers, sorted(countries)


def filter_servers(servers, country):
    filtered = [s for s in servers if s[0] == country]

    def parse_ping(ping):
        try:
            return int(ping.split()[0])
        except ValueError:
            return float("inf")

    filtered.sort(key=lambda s: parse_ping(s[1]))
    return filtered
