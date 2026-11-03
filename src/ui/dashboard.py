import time

from PySide6.QtCore import QPointF, Qt
from PySide6.QtGui import QColor, QPainter, QPalette, QRadialGradient
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class HeroPanel(QFrame):
    """A theme-aware radial glow for the connected-state hero."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("dashboardHero")
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground)

    def paintEvent(self, event):
        super().paintEvent(event)

        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        accent = self.palette().color(QPalette.ColorRole.WindowText)

        center = QPointF(self.rect().center())
        radius = max(self.width(), self.height()) * 0.72

        gradient = QRadialGradient(center, radius)

        inner = QColor(accent)
        inner.setAlpha(65)

        middle = QColor(accent)
        middle.setAlpha(20)

        outer = QColor(accent)
        outer.setAlpha(0)

        gradient.setColorAt(0.0, inner)
        gradient.setColorAt(0.55, middle)
        gradient.setColorAt(1.0, outer)

        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(gradient)
        painter.drawRoundedRect(self.rect(), 18, 18)

        painter.end()


def _metric_card(title):
    card = QFrame()
    card.setObjectName("dashboardCard")

    layout = QVBoxLayout(card)
    layout.setContentsMargins(14, 10, 14, 10)
    layout.setSpacing(5)

    heading = QLabel(title.upper())
    heading.setObjectName("dashboardMetricHeading")

    value = QLabel("—")
    value.setObjectName("dashboardMetricValue")
    value.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)

    layout.addWidget(heading)
    layout.addWidget(value)
    return card, value


def create_dashboard(window):
    page = QWidget()
    page.setObjectName("dashboardPage")

    # Main 2:1 horizontal layout
    layout = QHBoxLayout(page)
    layout.setContentsMargins(12, 12, 12, 12)
    layout.setSpacing(12)

    # ─────────────────────────────────────────
    # Left pane: Hero
    # ─────────────────────────────────────────

    hero = HeroPanel()

    hero_layout = QVBoxLayout(hero)
    hero_layout.setContentsMargins(24, 30, 24, 30)
    hero_layout.setSpacing(12)

    hero_layout.addStretch(1)

    window.dashboard_status_icon = QLabel("✓")
    window.dashboard_status_icon.setObjectName("dashboardHeroIcon")
    window.dashboard_status_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)

    window.dashboard_status = QLabel("CONNECTED")
    window.dashboard_status.setObjectName("dashboardStatus")
    window.dashboard_status.setAlignment(Qt.AlignmentFlag.AlignCenter)

    window.dashboard_country = QLabel("VPN")
    window.dashboard_country.setObjectName("dashboardCountry")
    window.dashboard_country.setAlignment(Qt.AlignmentFlag.AlignCenter)

    window.dashboard_hostname = QLabel("Waiting for server details…")
    window.dashboard_hostname.setObjectName("dashboardHostname")
    window.dashboard_hostname.setAlignment(Qt.AlignmentFlag.AlignCenter)
    window.dashboard_hostname.setTextInteractionFlags(
        Qt.TextInteractionFlag.TextSelectableByMouse
    )

    hero_layout.addWidget(window.dashboard_status_icon)
    hero_layout.addWidget(window.dashboard_status)
    hero_layout.addWidget(window.dashboard_country)
    hero_layout.addWidget(window.dashboard_hostname)

    hero_layout.addStretch(1)

    layout.addWidget(hero, 2)

    # ─────────────────────────────────────────
    # Right pane: Sidebar
    # ─────────────────────────────────────────

    sidebar = QFrame()
    sidebar.setObjectName("dashboardSidebar")

    sidebar_layout = QVBoxLayout(sidebar)
    sidebar_layout.setContentsMargins(14, 18, 14, 18)
    sidebar_layout.setSpacing(10)

    sidebar_title = QLabel("CONNECTION OVERVIEW")
    sidebar_title.setObjectName("dashboardSidebarTitle")

    sidebar_layout.addWidget(sidebar_title)

    # Metrics
    metric_specs = (
        ("SESSION", "dashboard_duration"),
        ("PING", "dashboard_ping"),
        ("SERVER IP", "dashboard_ip"),
        ("SPEED", "dashboard_speed"),
        ("USERS", "dashboard_users"),
        ("SCORE", "dashboard_score"),
    )

    for title, attribute in metric_specs:
        card, value = _metric_card(title)
        setattr(window, attribute, value)
        sidebar_layout.addWidget(card)

    sidebar_layout.addStretch(1)

    # Actions
    window.dashboard_copy_diagnostics_btn = QPushButton("Copy Diagnostics")
    window.dashboard_copy_diagnostics_btn.setObjectName("refreshButton")

    window.dashboard_logs_btn = QPushButton("Show Logs")
    window.dashboard_logs_btn.setObjectName("refreshButton")

    window.dashboard_disconnect_btn = QPushButton("Disconnect")
    window.dashboard_disconnect_btn.setObjectName("disconnectButton")

    sidebar_layout.addWidget(window.dashboard_copy_diagnostics_btn)
    sidebar_layout.addWidget(window.dashboard_logs_btn)
    sidebar_layout.addWidget(window.dashboard_disconnect_btn)

    window.dashboard_footer = QLabel("Connection details refresh automatically")
    window.dashboard_footer.setObjectName("dashboardFooter")
    window.dashboard_footer.setWordWrap(True)
    window.dashboard_footer.setAlignment(Qt.AlignmentFlag.AlignCenter)

    sidebar_layout.addWidget(window.dashboard_footer)

    layout.addWidget(sidebar, 1)

    return page


def update_dashboard(window, state):
    if not state:
        return

    window.dashboard_country.setText(state.get("country") or "VPN")
    window.dashboard_hostname.setText(state.get("hostname") or "Unknown server")
    window.dashboard_ip.setText(state.get("ip") or "Unknown")

    ping = state.get("ping")
    window.dashboard_ping.setText(f"{ping}" if ping is not None else "N/A")

    speed = state.get("speed")
    window.dashboard_speed.setText(f"{speed}" if speed is not None else "N/A")

    users = state.get("users")
    window.dashboard_users.setText(str(users) if users is not None else "N/A")

    score = state.get("score")
    window.dashboard_score.setText(str(score) if score is not None else "N/A")

    started_at = state.get("started_at")
    if started_at:
        elapsed = max(0, int(time.time() - started_at))
        hours, remainder = divmod(elapsed, 3600)
        minutes, seconds = divmod(remainder, 60)
        window.dashboard_duration.setText(f"{hours:02d}:{minutes:02d}:{seconds:02d}")
    else:
        window.dashboard_duration.setText("—")
