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
        self.box_height = self.box_width/2
        self.resize(self.box_width, self.box_height)

        # bg color
        self.off_color = QColor(142, 142, 147)
        self.on_color = QColor(52, 199, 89)

        # circle
        self.circle_color = QColor(229, 229, 234)
        self.radius_factor = 0.8

        # animation property
        self.anim_curve = QEasingCurve.InOutQuad
        self.anim_duration = 300

        # circle animation
        self._circle_center_x = self.height()/2
        self.anim_1 = QPropertyAnimation(self, b"circle_center_x", self)
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
    def circle_center_x(self):
        return self._circle_center_x



    @circle_center_x.setter
    def circle_center_x(self, center_x):
        cur = center_x
        end = self.anim_1.endValue()
        perc = cur/end
        on_center_x = max(self.width()-self.height()/2, self.width()/2)
        off_center_x = min(self.height()/2, self.width()/2)

        if self.isChecked():
            now_center_x = perc*on_center_x
        else:
            now_center_x = min(perc*off_center_x, on_center_x)

        self._circle_center_x = now_center_x
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
        self.anim_group.stop()

        if state:
            self.anim_1.setEndValue(max(self.width()-self.height()/2, self.width()/2))
            self.anim_2.setEndValue(self.on_color)
        else:
            self.anim_1.setEndValue(min(self.height()/2, self.width()/2))
            self.anim_2.setEndValue(self.off_color)

        self.anim_group.start()



    # paint
    def paintEvent(self, event):
        state = self.isChecked()

        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        p.setPen(Qt.NoPen)

        # roundeedRect
        rect = QRectF(0, 0 , self.width(), self.height())
        corner = float(self.height()/2)

        # ellipse radius
        radius = float(min(self.height()/2*self.radius_factor, self.width()/2*self.radius_factor))

        # ellipase center
        if self.anim_group.state() != QAbstractAnimation.Running:
            if state:
                self._circle_center_x = max(self.width()-self.height()/2, self.width()/2)
            else:
                self._circle_center_x = min(self.height()/2, self.width()/2)

        circle_center = QPointF(self._circle_center_x, self.height()/2)

        # start paint
        if state:
            # paint bg
            p.setBrush(self._bg_color)
            p.drawRoundedRect(rect, corner, corner)

            # paint circle
            p.setBrush(self.circle_color)
            p.drawEllipse(circle_center, radius, radius)

        else:
            # paint bg
            p.setBrush(self._bg_color)
            p.drawRoundedRect(rect, corner, corner)

            # paint circle
            p.setBrush(self.circle_color)
            p.drawEllipse(circle_center, radius, radius)

        # end paint
        p.end()



app = QApplication([])
toogleSwitchButton = ToggleSwitchButton()
toogleSwitchButton.show()
sys.exit(app.exec())
