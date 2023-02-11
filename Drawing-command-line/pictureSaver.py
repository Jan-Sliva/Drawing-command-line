import sys, os, random, json, cv2
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtCore import Qt, QEvent, QTimer, QRect
from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QFileDialog
from PyQt5.QtGui import QImage, QPen, QTabletEvent
import os.path as P
import numpy as np

from drawWindow import drawWindow
from siameseNetwork import siameseNetwork


class pictureSaver:

    
    def __init__(self):
        self.app = QtWidgets.QApplication(sys.argv)

        with open(P.join("settings", "settings.json"), 'r') as file:
            sett = json.loads(file.read())
        with open(P.join("settings", "data.json"), 'r') as file:
            self.data = json.loads(file.read())["commands"]

        self.canvasSize = (sett["X"], sett["Y"])
        self.crop = sett["crop"]

        self.window = drawWindow(self.canvasSize, sett["penWidth"], self.processImage, None)

        
        self.window.show()
        self.app.exec_()

    def processImage(self, img):
        
        img = img[self.crop:-self.crop, self.crop:-self.crop]
        img = cv2.resize(img, dsize=(32, 32), interpolation=cv2.INTER_AREA)
        
        fileName = QFileDialog.getSaveFileName(None, self.app.tr("Save drawing"),
                                       "pictures",
                                       self.app.tr("Images (*.png)"))

        try:
            cv2.imwrite(fileName[0], img)
        except:
            return
        self.app.quit()

