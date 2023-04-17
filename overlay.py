import sys

import win32api
from PyQt5 import QtGui, QtCore, uic
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget
from PyQt5.QtCore import (QCoreApplication, QObject, QRunnable, QThread,
                          QThreadPool, pyqtSignal)

import locator


class CalibratorWindow(QMainWindow):
    def __init__(self, parent=None, cal=None):
        super(CalibratorWindow, self).__init__(parent)
        self.get_top_left = False
        self.cal = cal
        self.setWindowFlags(
            QtCore.Qt.WindowStaysOnTopHint |
            QtCore.Qt.FramelessWindowHint |
            QtCore.Qt.X11BypassWindowManagerHint
        )


        widget = QtWidgets.QWidget()
        self.setStyleSheet("background-color: green;")
        self.move(0,0)
        hlayout = QtWidgets.QHBoxLayout(widget)
        a1 = QtWidgets.QLabel('We will now define the band in which footsteps will be displayed. \n\nUse a,s,d,w to place the top left corner of this box to the top left point of the desired \narea of the band'
                              'optimally this should be at the left side of the screen. \nThen press f.\nNow move the top left corner of this box to the bottom right corner of the desired band.\n'
                              'This should optimally be on the right hand side of the screen and a bit lower than before.\nAgain press f.\n\n Finally the programm will start and you will see marks, as soon as you hear sound.', self)
        a1.setStyleSheet("border: 1px solid black;background-color: yellow;font-size: 10pt;")
        hlayout.addWidget(a1)

        self.setCentralWidget(widget)

    def keyPressEvent(self, qKeyEvent):
        speed = 10
        if qKeyEvent.key() == QtCore.Qt.Key.Key_A:
            self.move(self.pos().x()-speed, self.pos().y())
        elif qKeyEvent.key() == QtCore.Qt.Key.Key_D:
            self.move(self.pos().x()+speed, self.pos().y())
        elif qKeyEvent.key() == QtCore.Qt.Key.Key_S:
            self.move(self.pos().x(), self.pos().y()+speed)
        elif qKeyEvent.key() == QtCore.Qt.Key.Key_W:
            self.move(self.pos().x(), self.pos().y()-speed)
        elif qKeyEvent.key() == QtCore.Qt.Key.Key_F:
            if self.get_top_left:
                self.cal.SCREEN_WIDTH = self.pos().x()-self.cal.SCREEN_LEFT
                self.cal.SCREEN_HEIGHT = self.pos().y()-self.cal.SCREEN_TOP
                QtCore.QCoreApplication.instance().quit()
            else:
                self.cal.SCREEN_LEFT = self.pos().x()
                self.cal.SCREEN_TOP = self.pos().y()
                self.get_top_left=True



class StepWindow(QMainWindow):
    def __init__(self, parent=None, cal=None):
        super(StepWindow, self).__init__(parent)
        self.cal = cal
        self.setWindowFlags(
            QtCore.Qt.WindowStaysOnTopHint |
            QtCore.Qt.FramelessWindowHint |
            QtCore.Qt.X11BypassWindowManagerHint
        )
        #self.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)
        self.setGeometry(self.cal.SCREEN_LEFT, self.cal.SCREEN_TOP, self.cal.SCREEN_WIDTH, self.cal.SCREEN_HEIGHT)
        self.size = min(self.cal.SCREEN_WIDTH, self.cal.SCREEN_HEIGHT)
        self.show_steps()

    def show_steps(self):
        self.thread = QtCore.QThread(self)
        self.thread.start()
        self.downloader = locator.LocatorThread(self)
        self.downloader.moveToThread(self.thread)
        self.downloader.show_angle_trigger.connect(self.show_step)
        self.thread.started.connect(self.downloader.run)
        self.thread.start()#downloader.start()

    @QtCore.pyqtSlot(float)
    def show_step(self, angle):
        print(angle)
        hor = self.cal.SCREEN_LEFT + (self.cal.SCREEN_WIDTH-self.size) * (0.5 + angle / (self.cal.ANGLE_RANGE * 2))
        hor = max(hor, self.cal.SCREEN_LEFT)
        hor = min(hor, self.cal.SCREEN_WIDTH + self.cal.SCREEN_LEFT)
        a1 = QtWidgets.QLabel(self)
        a1.resize(self.size, self.size)
        a1.setPixmap(QtGui.QPixmap('extra/step.png').scaled(self.size, self.size))
        a1.move(hor,0)

        a1.show()
        QtCore.QTimer.singleShot(200, a1.close)




def calibrate(cal):
    app = QApplication(sys.argv)
    mywindow = CalibratorWindow(cal=cal)
    mywindow.show()
    app.exec_()

def overlay(cal):
    app = QApplication(sys.argv)
    mywindow = StepWindow(cal=cal)
    mywindow.show()
    app.exec_()


