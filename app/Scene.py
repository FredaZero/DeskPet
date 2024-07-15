from PyQt6.QtWidgets import QApplication, QGraphicsProxyWidget, QGraphicsPixmapItem,QGraphicsScene, QGraphicsView, QPushButton, QVBoxLayout, QWidget, QLabel, QFrame
from PyQt6.QtCore import Qt, QEvent, QPointF, QPropertyAnimation, QVariantAnimation, QSize, QRectF, QTimer, QObject, QEasingCurve, pyqtSignal, QParallelAnimationGroup
from PyQt6.QtGui import QPainter, QImage, QPixmap, QBrush, QColor, QTransform, QIcon, QCursor, QMouseEvent
import pyautogui
import module
import Items
import random
from utils import RandomAnimation

class Movement(QGraphicsView):
    def __init__(self, scene):
        super(Movement, self).__init__(scene)
        self.scene = scene
        self.mouse_drag_pos = None
        self.is_follow_mouse = False
        self.mouse_moving = False
        self.screen = pyautogui.size()
        self.x_max = self.screen[0] - 48 # width of monitor
        self.y_max = self.screen[1] - 200 # height of monitor
        
        self.is_dragging = False
        self.drag_start_position = None
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
    ## Drag function
    def mousePressEvent(self, event: QMouseEvent):
        super().mousePressEvent(event)
        if event.button() == Qt.MouseButton.LeftButton:
            self.is_dragging = False
            self.drag_start_position = event.globalPosition().toPoint()
            self.mouse_drag_pos = event.globalPosition().toPoint() - self.parentWidget().pos()
            event.accept()

    def mouseMoveEvent(self, event: QMouseEvent):
        if not self.drag_start_position:
            return
        if (event.globalPosition().toPoint() - self.drag_start_position).manhattanLength() > 10:
            self.is_dragging = True
            new_pos = event.globalPosition().toPoint() - self.mouse_drag_pos
            self.parentWidget().move(new_pos)
            self.drag_start_position = event.globalPosition().toPoint()
            event.accept()

    def mouseReleaseEvent(self, event: QMouseEvent):
        super().mouseReleaseEvent(event)
        if not self.is_dragging:
            # Handle as click event if needed
            pass
        ## check if the deskpet is out of the screen boundary
        if event.globalPosition().toPoint().x() >= self.x_max: 
            print("*****Out of Boundary*****")
            delta_x = self.x_max - self.parentWidget().pos().x()
            self.parentWidget().move(1900-delta_x,event.globalPosition().toPoint().y() - self.mouse_drag_pos.y())
        elif event.globalPosition().toPoint().x() <=35:
            print("*****Out of Boundary*****")
            delta_x = 35 - self.parentWidget().pos().x()
            self.parentWidget().move(45-delta_x,event.globalPosition().toPoint().y() - self.mouse_drag_pos.y())
        elif event.globalPosition().toPoint().y() >= self.y_max:
            print("*****Out of Boundary*****")
            delta_y = self.y_max - self.parentWidget().pos().y()
            self.parentWidget().move(event.globalPosition().toPoint().x() - self.mouse_drag_pos.x(),949-delta_y)
        elif event.globalPosition().toPoint().y() <=20:
            print("*****Out of Boundary*****")
            delta_y = 20 - self.parentWidget().pos().y()
            self.parentWidget().move(event.globalPosition().toPoint().x() - self.mouse_drag_pos.x(),35-delta_y)
        self.is_dragging = False
        self.drag_start_position = None
        event.accept()


class MainScene(QWidget):
    def __init__(self) -> None:
        super(MainScene, self).__init__()

        self.switch = QPushButton()
        self.animation = None
        self.appear = None
        self.idle = None
        self.thinking = None
        self.menu = None
        self.is_dragging = False
        self.drag_start_position = None
        self.mouse_drag_pos = None
        self.is_follow_mouse = False
        self.mouse_moving = False
        self.scene = QGraphicsScene()
        
        

        self.init_ui()
        
        self.init_animation()
        

    def init_ui(self):
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute(0x78))
        self.setAutoFillBackground(True)

        rect = pyautogui.size()
        

        

        self.body_item = QPixmap("../img/BasicBody02.png").scaled(200, 200, Qt.AspectRatioMode.KeepAspectRatio)
        self.body = QGraphicsPixmapItem(self.body_item)
        self.body.setZValue(0)
        self.outfit_item = QPixmap(" ")
        self.outfit = QGraphicsPixmapItem(self.outfit_item)
        self.outfit.setZValue(1)
        self.scene.addItem(self.outfit)
        self.scene.addItem(self.body)
        

        # Define the position of the body
        body_pos = QPointF(100, 100)

        ### Add each body component to the scene
        self.ear1 = Items.Ear1Item()
        self.ear1_item = Items.EarGraphicsItem(self.ear1)
      
        
        self.ear1_item.setPos(body_pos + QPointF(-170, -180))
        self.scene.addItem(self.ear1_item) 

       
        self.ear2 = Items.Ear2Item()
        self.ear2_item = Items.EarGraphicsItem(self.ear2)
        self.ear2_item.setPos(body_pos + QPointF(60, -180))
        self.scene.addItem(self.ear2_item)

        self.eyes_item = Items.EyeItem()
        self.eyes = Items.EarGraphicsItem(self.eyes_item)
        self.eyes.setZValue(3)
        self.eyes.setOpacity(0.8)
        self.eyes.setPos(body_pos + QPointF(-35, -10))
        self.scene.addItem(self.eyes)

        self.item = QPixmap("../img/Foot2.png").scaled(50, 50, Qt.AspectRatioMode.KeepAspectRatio).transformed(QTransform().rotate(60))
        self.foot1 = QGraphicsPixmapItem(self.item)
        self.foot1.setZValue(1)
        self.foot1.setPos(body_pos + QPointF(-150, 100))
        self.scene.addItem(self.foot1)

        self.item = QPixmap("../img/Foot2.png").scaled(50, 50, Qt.AspectRatioMode.KeepAspectRatio).transformed(QTransform().rotate(-60))
        self.foot2 = QGraphicsPixmapItem(self.item)
        self.foot2.setZValue(1)
        self.foot2.setPos(body_pos + QPointF(100, 100))
        self.scene.addItem(self.foot2)

        proxy = QGraphicsProxyWidget()
        proxy.setWidget(self.switch)
        self.switch.resize(50, 50)
        self.switch.setStyleSheet("background-color: transparent")
        img = QImage()
        img.load("../img/Switch1.png")
        pixmap = QPixmap(img)
        SwitchIcon = QIcon(pixmap)
        self.switch.setIcon(SwitchIcon)
        self.switch.setIconSize(QSize(40, 40))
        proxy.setPos(body_pos + QPointF(-25, 20))
        proxy.setZValue(3)
        self.scene.addItem(proxy)

        ## ear animation
        self.ear1.clicked.connect(self.ear1_animate)
        self.ear2.clicked.connect(self.ear2_animate)
        
        ## Eye animation
        self.eyes_item.clicked.connect(self.eyes_animate)
        

        ## switch interaction
        self.switch.pressed.connect(self.switch_press)
        self.switch.released.connect(self.switch_release)

        view = Movement(self.scene)
        view.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignTop)
        view.setRenderHint(QPainter.RenderHint.Antialiasing)
        view.setStyleSheet("background-color: transparent; border: 0px")

        layout = QVBoxLayout()
        layout.addWidget(view)
        self.setLayout(layout)

        self.show()

    def init_animation(self):
        self.random_animation = RandomAnimation(self)

    def ear1_animate(self):
        print("Clicked!!!")
        pass

    def ear2_animate(self):
        print("Clicked!!!!")
        pass

    def eyes_animate(self):
        print("Clicked!!!")
        pass

    def auto_animation(self):
        pass

    def switch_press(self):
        self.switch.setStyleSheet("background-color: transparent")
        img = QImage()
        img.load("../img/Switch2.png")
        pixmap = QPixmap(img)
        SwitchIcon = QIcon(pixmap)
        self.switch.setIcon(SwitchIcon)
        self.switch.setIconSize(QSize(40, 40))
        if self.menu: # check if the menu exists
            self.switch.clicked.connect(self.menu.close)

    def switch_release(self):
        self.switch.setStyleSheet("background-color: transparent")
        img = QImage()
        img.load("../img/Switch1.png")
        pixmap = QPixmap(img)
        SwitchIcon = QIcon(pixmap)
        self.switch.setIcon(SwitchIcon)
        self.switch.setIconSize(QSize(40, 40))
        self.menu = MenuButton(QCursor.pos().x(), QCursor.pos().y(), self)
        self.menu.quit.clicked.connect(self.menu.close)

    


    

    
class MenuButton(QWidget):
    def __init__(self, x, y, parent):
        super(MenuButton,self).__init__()
        self.parent = parent
        if x <=1800:
            self.setGeometry(x+90, y-50,550,150)
        else:
            self.setGeometry(x-250, y-50,550,150)
        self.interface = QLabel(self)
        self.battery = QPushButton(self)
        self.battery.resize(50,50)
        self.battery.move(30,0)
        self.clothes = QPushButton(self)
        self.clothes.resize(50,50)
        self.clothes.move(130,0)
        self.wardrobe = None
        self.chat = QPushButton(self)
        self.chat.resize(50,50)
        self.ask = None
        self.chat.move(80,0)
        self.quit = QPushButton(self)
        self.quit.resize(50,50)
        self.quit.move(180,0)
       
        

        self.init_ui()
        self.clothes_change_window = module.ClothesChange(self.change_outfit)

    def init_ui(self):
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute(0x78))
        self.setAutoFillBackground(True)
        
        self.chat.setStyleSheet("background-color: transparent")
        chat_img = QPixmap("../img/Setup_notChose.png")
        chat_icon = QIcon(chat_img)
        self.chat.setIcon(chat_icon)
        self.chat.setIconSize(QSize(30,30))
        self.chat.clicked.connect(self.chatbox)

        self.battery.setStyleSheet("background-color: transparent")
        battery_img = QPixmap("../img/Battery_notChose.png")
        battery_icon = QIcon(battery_img)
        self.battery.setIcon(battery_icon)
        self.battery.setIconSize(QSize(30,30))

        self.clothes.setStyleSheet("background-color: transparent")
        clothes_img = QPixmap("../img/Clothes_NotChose.png")
        clothes_icon = QIcon(clothes_img)
        self.clothes.setIcon(clothes_icon)
        self.clothes.setIconSize(QSize(30,30))
        self.clothes.clicked.connect(self.open_wardrobe)

        

        
        self.quit.setStyleSheet("background-color: transparent")
        quit_img = QPixmap("../img/Exit_notChose.png")
        quit_icon = QIcon(quit_img)
        self.quit.setIcon(quit_icon)
        self.quit.setIconSize(QSize(30, 30))

        # Connect signals to change icon on press and revert on release
        self.quit.pressed.connect(self.on_quit_pressed)
        self.quit.released.connect(self.on_quit_released)



        self.show()

    def on_quit_pressed(self):
        # Change the icon to Exit_Chose when the button is pressed
        quit_img_chose = QPixmap("../img/Exit_Chose.png")
        quit_icon_chose = QIcon(quit_img_chose)
        self.quit.setIcon(quit_icon_chose)

    def on_quit_released(self):
        # Perform the quit action
        self.close()
        # Optionally, revert the icon back to Exit_notChose if the button remains visible after the action
        quit_img = QPixmap("../img/Exit_notChose.png")
        quit_icon = QIcon(quit_img)
        self.quit.setIcon(quit_icon)

    def close(self):
        self.hide()
        if self.ask is not None:
            self.ask.hide()
        if self.wardrobe is not None:
            self.wardrobe.hide()

    def chatbox(self):
        self.ask = module.ClippyChat()
        if self.ask.isHidden():
            self.ask.show()

    def open_wardrobe(self):
        
        if self.clothes_change_window.isHidden():
            self.clothes_change_window.show()
        print("changed!")
        
    def change_outfit(self, outfit_icon):
        if outfit_icon.strip():
            self.parent.outfit.setPixmap(QPixmap(outfit_icon).scaled(300, 300, Qt.AspectRatioMode.KeepAspectRatio))
            self.parent.outfit.setPos(QPointF(-50, -50))
        if outfit_icon != "original.png":
            self.parent.scene.removeItem(self.parent.ear1_item)
            self.parent.ear2_item.hide()