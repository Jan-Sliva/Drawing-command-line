import sys, os, random, json, cv2
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtCore import Qt, QEvent, QTimer, QRect
from PyQt5.QtWidgets import QApplication, QLabel, QPushButton
from PyQt5.QtGui import QImage, QPen, QTabletEvent
import os.path as P
import numpy as np

from drawWindow import drawWindow
from siameseNetwork import siameseNetwork


class drawingCommandLine:

    
    def __init__(self):
        self.app = QtWidgets.QApplication(sys.argv)

        with open(P.join("settings", "settings.json"), 'r') as file:
            sett = json.loads(file.read())
        with open(P.join("settings", "data.json"), 'r') as file:
            self.data = json.loads(file.read())["commands"]

        self.canvasSize = (sett["X"], sett["Y"])
        self.crop = sett["crop"]

        pictures = []

        for el in self.data:
            picPath = P.join("pictures", el["picture"])
            pictures.append(drawingCommandLine.readPicture(picPath))

        self.network = siameseNetwork(sett["network"], pictures)

        self.predIndex = None

        self.window = drawWindow(self.canvasSize, sett["penWidth"], self.processImage, self.processResponse)

        
        self.window.show()
        self.app.exec_()

    def quit(self):
        self.app.quit()

    # not implemented
    def openSettings(self):
        pass

    def processImage(self, img):
        img = self.imagePreprocessing(img)
        self.predIndex = self.network.predict(img)
        self.window.setQuestion(self.data[self.predIndex]["question"])

    def processCommand(self, command):
        if command == '$close':
            self.quit()
        elif command == '$settings':
            self.openSettings()
        else:
            try:
                os.system(command)
            except:
                print("Can't run " + command)

    def processResponse(self, res):
        self.window.setCanvas()
        if self.predIndex == None:    
            return
        if res:
            self.processCommand(self.data[self.predIndex]["command"])
        self.predIndex = None

    def imagePreprocessing(self, img):
        # to black and white
        img = np.sum(img, 2) / 3

        img = img[self.crop:-self.crop, self.crop:-self.crop]
        img = cv2.resize(img, dsize=(32, 32), interpolation=cv2.INTER_AREA)
        img = np.reshape(img, (32, 32, 1))
        img = img.astype("float32") / 255
        return img


    @staticmethod
    def readPicture(path):
        img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
        img = np.reshape(img, (32, 32, 1))
        img = img.astype("float32") / 255
        return img

