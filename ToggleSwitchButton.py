from PySide6.QtWidgets import QApplication, QCheckBox
from PySide6.QtGui import QPainter, QColor, QBrush
from PySide6.QtCore import (Qt, Property, QEasingCurve, QPropertyAnimation,
        QPointF, QRectF, QAbstractAnimation, QParallelAnimationGroup)

import sys



class ToggleSwitchButton(QCheckBox):
    def __init__(self):
        super().__init__()

        # window size
        self.box_width = 120
        self.box_height = self.box_width / 2
        # self.setWindowFlags(Qt.FramelessWindowHint)
        # self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.resize(self.box_width, self.box_height)

        # bg color
        self.off_color = QColor(142, 142, 147)
        self.on_color = QColor(52, 199, 89)

        # circle
        self.circle_color = QColor(242, 242, 247)
        self.radius_factor = 0.8

        # animation property
        self.anim_curve = QEasingCurve.OutBounce
        self.anim_duration = 300

        # circle animation
        self._pos_factor = 0
        self.anim_1 = QPropertyAnimation(self, b"pos_factor", self)
        self.anim_1.setEasingCurve(self.anim_curve)
        self.anim_1.setDuration(self.anim_duration)

        # bg color animation
        self._bg_color = self.off_color
        self.anim_2 = QPropertyAnimation(self, b"bg_color", self)
        self.anim_2.setEasingCurve(self.anim_curve)
        self.anim_2.setDuration(self.anim_duration)

        # animation group
        self.anim_group = QParallelAnimationGroup()
        self.anim_group.addAnimation(self.anim_1)
        self.anim_group.addAnimation(self.anim_2)

        # emit a signal
        self.toggled.connect(self.start_anim)



    @Property(float)
    def pos_factor(self):
        return self._pos_factor



    @pos_factor.setter
    def pos_factor(self, value):
        self._pos_factor = value
        self.update()



    @Property(QColor)
    def bg_color(self):
        return self._bg_color



    @bg_color.setter
    def bg_color(self, color):
        self._bg_color = color
        self.update()



    # mouse area
    def hitButton(self, pos):
        return self.contentsRect().contains(pos)



    # start animation
    def start_anim(self, state):
        # stop animation
        self.anim_group.stop()

        if state:
            self.anim_1.setEndValue(1)
            self.anim_2.setEndValue(self.on_color)
        else:
            self.anim_1.setEndValue(0)
            self.anim_2.setEndValue(self.off_color)

        # start animation
        self.anim_group.start()



    # paint
    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        p.setPen(Qt.NoPen)

        # roundeedRect
        rect = QRectF(0, 0 , self.width(), self.height())
        corner = min(self.height() / 2, self.width() / 2)

        # circle radius
        radius = min(self.height(), self.width()) / 2 * self.radius_factor

        # circle cneter x
        lengths = max(self.width() - self.height(), 0)
        circle_center_x = min(self.height() / 2, self.width() / 2) + lengths * self._pos_factor

        # circle center
        circle_center = QPointF(circle_center_x, self.height() / 2)

        # paint bg
        p.setBrush(self._bg_color)
        p.drawRoundedRect(rect, corner, corner)

        # paint circle
        p.setBrush(self.circle_color)
        p.drawEllipse(circle_center, radius, radius)

        print(circle_center, radius, lengths)
        # end paint
        p.end()



app = QApplication([])
toogleSwitchButton = ToggleSwitchButton()
toogleSwitchButton.show()
sys.exit(app.exec())
