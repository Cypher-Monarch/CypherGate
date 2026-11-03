import math
import time

from PySide6.QtCore import QPointF, Qt, QTimer
from PySide6.QtGui import QColor, QPainter, QPalette, QPen, QRadialGradient
from PySide6.QtWidgets import (
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class ConnectionOrb(QWidget):
    """A subtle, theme-aware pulse for the connected-state hero."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(104, 104)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self._phase = 0.0

        self._timer = QTimer(self)
        self._timer.timeout.connect(self._advance)
        self._timer.start(45)

    def _advance(self):
        self._phase = (self._phase + 0.045) % (math.pi * 2)
        self.update()

    def paintEvent(self, event):
        del event
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        center = QPointF(self.rect().center())
        accent = QColor(self.palette().color(QPalette.ColorRole.WindowText))
        pulse = (math.sin(self._phase) + 1) / 2

        glow = QRadialGradient(center, 48 + pulse * 5)
        inner = QColor(accent)
        inner.setAlpha(58)
        outer = QColor(accent)
        outer.setAlpha(0)
        glow.setColorAt(0.0, inner)
        glow.setColorAt(1.0, outer)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(glow)
        painter.drawEllipse(center, 49, 49)

        ring = QColor(accent)
        ring.setAlpha(105 + int(pulse * 55))
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.setPen(QPen(ring, 1.5))
        painter.drawEllipse(center, 35 + pulse * 2, 35 + pulse * 2)

        painter.setPen(QPen(accent, 2.5))
        painter.drawEllipse(center, 27, 27)
        painter.setPen(accent)
        font = painter.font()
        font.setPixelSize(29)
        font.setBold(True)
        painter.setFont(font)
        painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, "✓")


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

    layout = QVBoxLayout(page)
    layout.setContentsMargins(12, 18, 12, 12)
    layout.setSpacing(14)

    # Hero section
    hero = QFrame()
    hero.setObjectName("dashboardHero")
    hero_layout = QVBoxLayout(hero)
    hero_layout.setContentsMargins(20, 22, 20, 22)
    hero_layout.setSpacing(7)

    window.dashboard_status_icon = ConnectionOrb()

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

    layout.addWidget(hero)

    # Session and server metrics
    metrics = QGridLayout()
    metrics.setHorizontalSpacing(10)
    metrics.setVerticalSpacing(10)

    metric_specs = (
        ("SESSION DURATION", "dashboard_duration"),
        ("SERVER PING", "dashboard_ping"),
        ("SERVER IP", "dashboard_ip"),
        ("ADVERTISED SPEED", "dashboard_speed"),
        ("SERVER USERS", "dashboard_users"),
        ("SERVER SCORE", "dashboard_score"),
    )

    for index, (title, attribute) in enumerate(metric_specs):
        card, value = _metric_card(title)
        setattr(window, attribute, value)
        metrics.addWidget(card, index // 2, index % 2)

    layout.addLayout(metrics)
    layout.addStretch(1)

    # Dashboard actions
    actions = QHBoxLayout()
    actions.setSpacing(10)

    window.dashboard_logs_btn = QPushButton("Show Logs")
    window.dashboard_logs_btn.setObjectName("refreshButton")

    window.dashboard_disconnect_btn = QPushButton("Disconnect")
    window.dashboard_disconnect_btn.setObjectName("disconnectButton")

    actions.addWidget(window.dashboard_logs_btn)
    actions.addWidget(window.dashboard_disconnect_btn)
    layout.addLayout(actions)

    window.dashboard_footer = QLabel("Connection details are refreshed automatically")
    window.dashboard_footer.setObjectName("dashboardFooter")
    window.dashboard_footer.setAlignment(Qt.AlignmentFlag.AlignCenter)
    layout.addWidget(window.dashboard_footer)

    return page


def update_dashboard(window, state):
    if not state:
        return

    window.dashboard_country.setText(state.get("country") or "VPN")
    window.dashboard_hostname.setText(state.get("hostname") or "Unknown server")
    window.dashboard_ip.setText(state.get("ip") or "Unknown")

    ping = state.get("ping")
    window.dashboard_ping.setText(f"{ping} ms" if ping is not None else "N/A")

    speed = state.get("speed")
    window.dashboard_speed.setText(f"{speed} Mbps" if speed is not None else "N/A")

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
