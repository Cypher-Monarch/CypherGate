from PySide6.QtCore import (
    QEasingCurve,
    QPropertyAnimation,
    QRectF,
    QSize,
    QTimer,
)

from PySide6.QtWidgets import (
    QGraphicsOpacityEffect,
    QSystemTrayIcon,
)

# ────────────────────────────────────────────────────────
# Animation Methods
# ────────────────────────────────────────────────────────


def animated_exit(self, action="close"):
    self.effect = QGraphicsOpacityEffect(self)
    self.setGraphicsEffect(self.effect)

    self.fade = QPropertyAnimation(self.effect, b"opacity")
    self.fade.setDuration(300)
    self.fade.setStartValue(1)
    self.fade.setEndValue(0)
    self.fade.setEasingCurve(QEasingCurve.InOutQuad)

    if action == "minimize":
        self.geo = self.geometry()
        self.shrink = QPropertyAnimation(self, b"geometry")
        self.shrink.setDuration(300)
        self.shrink.setStartValue(self.geo)
        self.shrink.setEndValue(QRectF(self.geo.center(), QSize(1, 1)).toRect())
        self.shrink.setEasingCurve(QEasingCurve.InOutCubic)

        self.fade.start()
        self.shrink.start()
        self.fade.finished.connect(self.final_minimize)
    elif action == "close":
        self.fade.start()
        self.fade.finished.connect(self.final_close)


def on_tray_icon_activated(self, reason):
    if reason == QSystemTrayIcon.DoubleClick:
        if hasattr(self, "original_geometry"):
            self.tray_restore()


def tray_restore(self):
    self.setVisible(True)
    self.showNormal()
    self.raise_()
    self.activateWindow()
    self.setWindowOpacity(1)


def animated_restore(self):
    self.setWindowOpacity(0)
    self.show()

    def start_animation():
        if not hasattr(self, "original_geometry"):
            self.original_geometry = self.geometry()

        start_rect = QRectF(self.original_geometry.center(), QSize(10, 10)).toRect()
        self.setGeometry(start_rect)

        geo_anim = QPropertyAnimation(self, b"geometry", self)
        geo_anim.setStartValue(start_rect)
        geo_anim.setEndValue(self.original_geometry)
        geo_anim.setDuration(400)
        geo_anim.setEasingCurve(QEasingCurve.OutBack)

        opacity_anim = QPropertyAnimation(self, b"windowOpacity", self)
        opacity_anim.setStartValue(0)
        opacity_anim.setEndValue(1)
        opacity_anim.setDuration(400)
        opacity_anim.setEasingCurve(QEasingCurve.InOutQuad)

        geo_anim.start()
        opacity_anim.start()

    QTimer.singleShot(10, start_animation)


def start_spinner(self):
    self.spinner.show()


def stop_spinner(self, final_status):
    self.spinner.hide()
    self.status_label.setText(final_status)


def final_close(self):
    self.close()


def final_minimize(self):
    self.showMinimized()
    self.setGraphicsEffect(None)
