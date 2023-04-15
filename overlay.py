import sys

from PyQt5 import QtGui, QtCore, uic
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication



class StepWindow(QMainWindow):
    def __init__(self, parent=None, angle=0, cal=None):
        super(StepWindow, self).__init__(parent)
        QtCore.QTimer.singleShot(2000, self.close)

        self.move(0,0)

        self.setWindowFlags(
            QtCore.Qt.WindowStaysOnTopHint |
            QtCore.Qt.FramelessWindowHint |
            QtCore.Qt.X11BypassWindowManagerHint
        )

        hor = cal.SCREEN_LEFT + cal.SCREEN_WIDTH*(0.5+angle/(cal.ANGLE_RANGE*2))
        hor = max(hor, cal.SCREEN_LEFT)
        hor = min(hor, cal.SCREEN_WIDTH+cal.SCREEN_LEFT)
        self.move(hor, cal.SCREEN_TOP+cal.SCREEN_HEIGHT-300)
        print(angle)
        print(angle/(cal.ANGLE_RANGE*2))
        print((0.5+angle/(cal.ANGLE_RANGE*2)))
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)


        widget = QtWidgets.QWidget()

        hlayout = QtWidgets.QHBoxLayout(widget)

        a1 = QtWidgets.QLabel()
        a1.setPixmap(QtGui.QPixmap('extra/step.png').scaledToWidth(500))

        hlayout.addWidget(a1)
        hlayout.addStretch()

        self.setCentralWidget(widget)



def show_at_angle(angle, cal):
    app = QApplication(sys.argv)
    mywindow = StepWindow(angle=angle, cal=cal)
    mywindow.show()
    app.exec_()


