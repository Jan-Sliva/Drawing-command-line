import sys, os, random
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtCore import Qt, QEvent, QTimer, QRect
from PyQt5.QtWidgets import QApplication, QLabel, QPushButton
from PyQt5.QtGui import QImage, QPen, QTabletEvent

from canvas import canvas

class drawWindow(QtWidgets.QMainWindow):

    def __init__(self, canvasSize, penWidth, processImage, processResponse):
        super().__init__()

        self.setWindowFlag(Qt.FramelessWindowHint) # hide the title bar

        self.processResponse = processResponse
        self.canvasSize = canvasSize
        self.penWidth = penWidth
        self.processImage = processImage

        self.setCanvas()

    def setCanvas(self):
        thisCanvas = canvas(self.canvasSize, self.penWidth, self.processImage)

        l = QtWidgets.QVBoxLayout()
        l.addWidget(thisCanvas)
        
        w = QtWidgets.QWidget()
        w.setLayout(l)
        self.setCentralWidget(w)

    def onYesPressed(self):
        self.processResponse(True)

    def onNoPressed(self):
        self.processResponse(False)

    def setQuestion(self, question):
        l = QtWidgets.QVBoxLayout()

        label = QLabel(question)
        label.setWordWrap(True)
        l.addWidget(label)

        button1 = QPushButton('Yes')
        button1.clicked.connect(self.onYesPressed)
        l.addWidget(button1)

        button2 = QPushButton('No')
        button2.clicked.connect(self.onNoPressed)
        l.addWidget(button2)

        w = QtWidgets.QWidget()
        w.setFixedSize(*self.canvasSize)
        w.setLayout(l)
        self.setCentralWidget(w)
        


    

