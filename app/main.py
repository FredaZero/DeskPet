from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QMenu, QSystemTrayIcon
from PyQt6.QtGui import QIcon, QPixmap, QMovie, QAction
from PyQt6.QtCore import *
import sys
import Scene


class DeskPet(QWidget):
    def __init__(self):
        super(DeskPet,self).__init__()
        self.icon = None
        self.base = None
        self.ears = None
        self.eyes = None
        self.tray_icon_menu = None
        self.pet = None
        self.set_up()
        #self.initPall()
    def set_up(self):
        self.icon = QAction("Quit",self,triggered=QApplication.instance().quit)
        self.icon.setIcon(QIcon("../img/exit_icon.png"))
        self.tray_icon_menu = QMenu(self)
        self.tray_icon_menu.addAction(self.icon)

        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon("../img/Sakura.png"))
        self.tray_icon.setContextMenu(self.tray_icon_menu)
        self.tray_icon.show()
        self.pet = Scene.MainScene() #ControlPet.PetControl()




if __name__=="__main__":
    app = QApplication(sys.argv)
    pet = DeskPet()
    sys.exit(app.exec())


