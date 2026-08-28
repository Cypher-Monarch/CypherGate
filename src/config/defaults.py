DEFAULT_SETTINGS = {
    "config_version": 1,
    "theme": {
        "mode": "builtin",
        "name": "pastel-orange",
        "path": None,
    },
    "icons": {
        "size": {
            "cancel": 20,
            "refresh": 20,
            "connect": 20,
            "disconnect": 20,
            "auto_connect": 20,
            "show": 20,
            "exit": 20,
            "tray": {
                "cancel": 20,
                "connect": 20,
                "disconnect": 20,
                "show": 20,
                "exit": 20,
            },
        },
        "color": {
            "cancel": "#E06C75",
            "refresh": "#D4AF37",
            "connect": "#0F0F0F",
            "disconnect": "#E06C75",
            "auto_connect": "#D4AF37",
            "show": "#D4AF37",
            "exit": "#E06C75",
            "tray": {
                "cancel": "#E06C75",
                "connect": "#D4AF37",
                "disconnect": "#E06C75",
                "show": "#D4AF37",
                "exit": "#E06C75",
            },
        },
    },
    "widgets": {
        "spinner": {
            "size": 40,
            "color": "#FFD700",
            "thickness": 3,
            "fps": 60,
            "rotation_speed": 360,
        },
        "table": {
            "columns": [
                "country",
                "ping",
                "speed",
                "users",
            ],
            "sort_by": "ping",
            "sort_order": "ascending",
        },
    },
    "application": {
        "minimize_to_tray": True,
        "notifications": True,
        "status_update_interval": 500,
        "use_custom_fonts": True,
    },
    "vpn": {
        "connection_timeout": 15,
        "default_country": None,
    },
}
