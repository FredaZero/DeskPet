from PyQt6.QtWidgets import QApplication, QGraphicsProxyWidget, QGraphicsPixmapItem,QGraphicsScene, QGraphicsView, QPushButton, QVBoxLayout, QWidget, QLabel, QFrame
from PyQt6.QtCore import Qt, QEvent, QPointF, QPropertyAnimation, QVariantAnimation, QSize, QRectF, QTimer, QObject, QEasingCurve, pyqtSignal, QParallelAnimationGroup
from PyQt6.QtGui import QPainter, QImage, QPixmap, QBrush, QColor, QTransform, QIcon, QCursor, QMouseEvent
import pyautogui
import module
import Items
import random


#########
## Animation
#########
class RandomAnimation(QWidget):
    def __init__(self,parent=None) -> None:
        super(RandomAnimation, self).__init__()
        self.parent = parent
        self.animation = None
        self.appear = None
        self.idle = None
        self.thinking = None
        self.event_number = 2
        self.state = 1
        self.i_frame = 0
        self.frame = QFrame(self)

        self.get_actions()
        self.set_state()
        self.parent.update()


    def load_png(self, images):
        pic_arr = []
        for image in images:
            img = QImage()
            print('img/' + image)
            img.load('img/' + image)
            pic_arr.append(img)
        return pic_arr
    
    def get_actions(self):
        self.idle = self.load_png(["idle1.png","idle2.png","idle2.png","idle2.png","open_eye3.png","idle1.png","open_eye3.png","idle1.png"])
        self.appear = self.load_png(["body.png","open_eye1.png","open_eye2.png",
                                     "open_eye1.png","open_eye2.png","ear_shaking2.png","ear_shaking1.png","ear_shaking3.png","idle1.png",
                                     "ear_shaking4.png","ear_shaking3.png","ear_shaking5.png","idle1.png"])

    def set_state(self):
        if self.event_number == 1:
            self.state = 0
            QTimer.singleShot(900,self.update)
            
        else:
            self.state = 1
           
            QTimer.singleShot(3000,self.update)

    def update(self):
       ## update frame according to the current state
        if self.state == 0:
            self.frame = self.appear[self.i_frame]
            self.animate(self.appear,2,4)
            self.parent.body_item.setPixmap(QPixmap.fromImage(self.frame).scaled(300,300,Qt.AspectRatioMode.KeepAspectRatio))
        elif self.state == 1:
            self.frame = self.idle[self.i_frame]
            self.animate(self.idle,2,4)

        
        QTimer.singleShot(600,self.set_state)

    def animate(self,array,a,b):
        if self.i_frame < len(array) - 1:
            self.i_frame += 1
        else:
            self.i_frame = 0
            self.event_number = random.randint(a,b)
       ## default animaiton: eye blinking
        self.parent.eyes_item.animation.setStartValue(1.0)
        self.parent.eyes_item.animation.setKeyValueAt(0.25, 0.5)
        self.parent.eyes_item.animation.setKeyValueAt(0.5, 0)
        self.parent.eyes_item.animation.setKeyValueAt(0.75, 0.5)
        self.parent.eyes_item.animation.setEndValue(1.0)
        self.parent.eyes_item.animation.setLoopCount(2)
        self.parent.eyes_item.animation.setDuration(500)
        self.parent.eyes_item.animation.start()
        print("Eye blinking")