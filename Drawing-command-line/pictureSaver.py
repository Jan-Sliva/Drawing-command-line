import sys, os, random, json, cv2
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtCore import Qt, QEvent, QTimer, QRect
from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QFileDialog, QLineEdit
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


        l = QtWidgets.QVBoxLayout()

        label = QLabel("What do you want to draw?")
        label.setWordWrap(True)
        l.addWidget(label)

        self.textbox = QLineEdit()
        l.addWidget(self.textbox)

        button2 = QPushButton('Submit')
        button2.clicked.connect(self.onSubmit)
        l.addWidget(button2)

        w = QtWidgets.QWidget()
        w.setFixedSize(*self.canvasSize)
        w.setLayout(l)
        self.window.setCentralWidget(w)

        
        self.window.show()
        self.app.exec_()

    def onSubmit(self):
        self.saveAs = P.join("pictures", self.textbox.text())
        if not os.path.exists(self.saveAs):
            os.mkdir(self.saveAs)
        self.num = 1
        self.window.setCanvas()


    def processImage(self, img):
        
        img = img[self.crop:-self.crop, self.crop:-self.crop]
        img = cv2.resize(img, dsize=(32, 32), interpolation=cv2.INTER_AREA)
        
        while os.path.exists(P.join(self.saveAs, str(self.num) + ".png")):
            self.num +=1
        
        fileName = P.join(self.saveAs, str(self.num) + ".png")

        try:
            cv2.imwrite(fileName, img)
        except Exception as e:
            print(e)
            return
        
        # self.app.quit()

