import sys, os, random
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtCore import Qt, QEvent, QTimer, QRect
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QImage, QPen, QTabletEvent
import numpy as np


class canvas(QtWidgets.QLabel):
    def __init__(self, canvasSize, penWidth, processImage):
        super().__init__()

        self.processImage = processImage
        self.canvasSize = canvasSize
        self.penWidth = penWidth

        pixmap = QtGui.QPixmap(*self.canvasSize)
        self.setPixmap(pixmap)

        self.pixmap().fill(Qt.white)
        self.setPixmap(self.pixmap())

        self.timer = QTimer()
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.endMove)

        self.zamek = QTimer()
        self.zamek.setSingleShot(True)

        self.last_x, self.last_y = None, None

        self.leftStylus = False

    @staticmethod
    def QPixmapToArray(pixmap):
        size = pixmap.size()
        h = size.width()
        w = size.height()

        qimg = pixmap.toImage()
        b = qimg.bits()
        b.setsize(w*h*4)

        img = np.frombuffer(b, dtype=np.uint8).reshape((w,h,4)).copy()
        img = img[:, :, :3]
        
        return img
        


    def clearCanvas(self):
        painter = QtGui.QPainter(self.pixmap())
        painter.fillRect(0, 0, *self.canvasSize, Qt.white)
        painter.end()
        self.update()


    def acceptImage(self):
        pict = self.pixmap()
        pict = canvas.QPixmapToArray(pict)
        self.processImage(pict)

        self.clearCanvas()

    def endMove(self):
        self.last_x = None
        self.last_y = None
        if self.zamek.isActive():
            self.zamek.stop()


    def mousePressEvent(self, ev: QtGui.QMouseEvent) -> None:
        if ev.button() == Qt.RightButton:
            self.acceptImage()
        elif ev.button() == Qt.MidButton:
            self.clearCanvas()

    def mouseMoveEvent(self, e: QtGui.QMouseEvent) -> None:
        if (e.buttons() & Qt.LeftButton):
            if self.last_x is None:
                self.last_x = e.x()
                self.last_y = e.y()
                return

            painter = QtGui.QPainter(self.pixmap())
            painter.setPen(QPen(Qt.black, self.penWidth))
            painter.drawLine(self.last_x, self.last_y, e.x(), e.y())
            painter.end()
            self.update()

            self.last_x = e.x()
            self.last_y = e.y()

    def mouseReleaseEvent(self, e: QtGui.QMouseEvent) -> None:
        if e.button() == Qt.LeftButton:
            self.endMove()

    def tabletEvent(self, e: QtGui.QTabletEvent) -> None:
        global Správce
        
        if e.type() == QEvent.TabletPress:
            if e.button() == Qt.RightButton:
                self.acceptImage()

            elif e.button() == Qt.LeftButton:
                if self.timer.isActive():
                    if self.leftStylus:
                        self.leftStylus = False
                    else:
                        self.clearCanvas()

                        self.last_x = None
                        self.last_y = None
                        self.zamek.start(300)

                        self.leftStylus = True
                    self.timer.stop()
        elif e.type() == QEvent.TabletRelease and e.button() == Qt.LeftButton:
            self.timer.start(20)
        elif (e.type() == QEvent.TabletMove) and (e.buttons() & Qt.LeftButton) and (not self.zamek.isActive()):
            if self.last_x is None:
                self.last_x = e.x()
                self.last_y = e.y()
                return

            painter = QtGui.QPainter(self.pixmap())
            painter.setPen(QPen(Qt.black, self.penWidth))
            painter.drawLine(self.last_x, self.last_y, e.x(), e.y())
            painter.end()
            self.update()

            self.last_x = e.x()
            self.last_y = e.y()
