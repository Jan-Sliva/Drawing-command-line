import sys, os, random
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtCore import Qt, QEvent, QTimer, QRect
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QImage, QPen, QTabletEvent


ROZMERY = (192, 192)
# ROZMERY = (500, 500)
TLOUŠŤKA = 2    
FOLDER = "dataSet"

testList = [\
     ["Chrome", "chrome", 50],\
     ["VS Code", "vscode", 50],\
     ["Složka", "fileExplorer", 50],\
     ["Texmaker", "texmaker", 50],\
     ["WiFi", "wifi", 50],\
     ["One Note", "oneNote", 50],\
     ["Jas", "brightness", 50],\
     ["Hlasitost", "volume", 50],\
     ["Ticho", "mute", 50],\
     ["Skype", "skype", 50],\
     ["Zavřít", "close", 50],\
     ["Nastavení", "settings", 50]
    ]

class správceSložky():
    def __init__(self, jméno, složka, maxPočet) -> None:
        self.jméno = jméno
        self.složka = složka
        if not os.path.exists(self.složka):
            os.makedirs(self.složka)
        self.maxPočet = maxPočet
        self.index = 0
        self.dostupné = None
        self.aktualizujIndex()

    def aktualizujIndex(self) -> bool:
        soubory = os.listdir(self.složka)
        while (str(self.index) + ".png") in soubory:
            self.index += 1
        self.dostupné = self.index < self.maxPočet

    def dejNázevSouboru(self):
        return os.path.join(self.složka, str(self.index) + ".png")

    def další(self):
        self.index += 1
        self.aktualizujIndex()

class správceDataSetu():
    def __init__(self, seznam, složka):
        self.složka = složka
        if not os.path.exists(self.složka):
            os.makedirs(self.složka)

        self.ukončeno = False

        self.seznamSprávců = []
        for prvek in seznam:
            správce = správceSložky(prvek[0], os.path.join(self.složka, prvek[1]), prvek[2])
            if správce.dostupné:
                self.seznamSprávců.append(správce)
        
        if len(self.seznamSprávců) == 0:
            self.ukončeno = True
        else:
            self.index = random.randint(0, len(self.seznamSprávců) - 1)

    def další(self):
        if self.ukončeno:
            return

        self.seznamSprávců[self.index].další()
        if not self.seznamSprávců[self.index].dostupné:
            self.seznamSprávců.pop(self.index)
        if len(self.seznamSprávců) == 0:
            self.ukončeno = True
            return
        self.index = random.randint(0, len(self.seznamSprávců) - 1)

    def dejJméno(self):
        if self.ukončeno:
            return "Konec"
        return self.seznamSprávců[self.index].jméno

    def dejNázevSouboru(self):
        if self.ukončeno:
            return ""
        return self.seznamSprávců[self.index].dejNázevSouboru()


Správce = správceDataSetu(testList, FOLDER)

class Canvas(QtWidgets.QLabel):
    def __init__(self, nastavNapis):
        super().__init__()

        self.nastavNapis = nastavNapis

        pixmap = QtGui.QPixmap(*ROZMERY)
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

    def endMove(self):
        self.last_x = None
        self.last_y = None
        if self.zamek.isActive():
            self.zamek.stop()


    def tabletEvent(self, e: QtGui.QTabletEvent) -> None:
        global Správce
        
        if e.type() == QEvent.TabletPress:
            if e.button() == Qt.RightButton:
                if not Správce.ukončeno:
                    self.pixmap().save(Správce.dejNázevSouboru())

                painter = QtGui.QPainter(self.pixmap())
                painter.fillRect(0, 0, *ROZMERY, Qt.white)
                painter.end()
                self.update()

                Správce.další()

                self.nastavNapis(Správce.dejJméno())
            elif e.button() == Qt.LeftButton:
                if self.timer.isActive():
                    if self.leftStylus:
                        self.leftStylus = False
                    else:
                        painter = QtGui.QPainter(self.pixmap())
                        painter.fillRect(0, 0, *ROZMERY, Qt.white)
                        painter.end()
                        self.update()

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
            painter.setPen(QPen(Qt.black, TLOUŠŤKA))
            painter.drawLine(self.last_x, self.last_y, e.x(), e.y())
            painter.end()
            self.update()

            self.last_x = e.x()
            self.last_y = e.y()

class CoKreslit(QtWidgets.QLabel):
    def __init__(self):
        super().__init__()

        pixmap = QtGui.QPixmap(ROZMERY[0], int(ROZMERY[0]/5))
        self.setPixmap(pixmap)

        self.nastavNapis(Správce.dejJméno())

    def nastavNapis(self, coNapsat):
        
        painter = QtGui.QPainter(self.pixmap())
        painter.setPen(QPen(Qt.black))
        font = painter.font()
        font.setPointSize(int(ROZMERY[0]/13))
        painter.setFont(font)

        rect = QRect(0,0,ROZMERY[0], int(ROZMERY[0]/5)) 
        painter.fillRect(rect, Qt.white)
        painter.drawText(rect, Qt.AlignCenter, coNapsat)
        painter.end()
        self.update()

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()

        self.coKreslit = CoKreslit()
        self.canvas = Canvas(self.coKreslit.nastavNapis)

        w = QtWidgets.QWidget()
        l = QtWidgets.QVBoxLayout()
        w.setLayout(l)
        l.addWidget(self.coKreslit)
        l.addWidget(self.canvas)

        self.setCentralWidget(w)

app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()