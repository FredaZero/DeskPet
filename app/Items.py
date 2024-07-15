import sys
from PyQt6.QtWidgets import (QApplication, QGraphicsView, QGraphicsScene,
QGraphicsPixmapItem, QGraphicsObject, QGraphicsItem)
from PyQt6.QtCore import (Qt, QObject, QPointF, QRectF,
QPropertyAnimation, pyqtProperty, pyqtSignal, QByteArray, QEasingCurve)
from PyQt6.QtGui import QPixmap, QTransform, QMouseEvent
import Items

class Ear1Item(QObject):
    clicked = pyqtSignal()  # Add the clicked signal

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self._rotation = -20
        self._rotated_pixmap = None
        self._pixmap = QPixmap(f"../img/Ears2.png").scaled(120, 120, Qt.AspectRatioMode.KeepAspectRatio).transformed(QTransform().rotate(self._rotation))
        
        self.animation = QPropertyAnimation(self, b"rotation")
        self.animation.setDuration(200)
        
    @pyqtProperty(int)
    def rotation(self):
        return self._rotation
    
    @rotation.setter
    def rotation(self, value):
        self._rotation = value
        transform = QTransform()
        transform.rotate(self._rotation)
        self._rotated_pixmap = self._pixmap.transformed(transform)
        if self.parent:
            self.parent.update()

    def boundingRect(self):
        
        return QRectF(-72, -0.2*self._pixmap.height(),
                      3.2*self._pixmap.width(), 1.3*self._pixmap.height())

    def paint(self, painter, option, widget):
        
        painter.translate(self._pixmap.width() / 2, self._pixmap.height())
        painter.rotate(self._rotation)
        painter.drawPixmap(-self._pixmap.width() / 2, -self._pixmap.height(), self._pixmap)
    
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            
            self.clicked.emit()  # Emit the clicked signal
            self.animation.setStartValue(-20)
            self.animation.setKeyValueAt(0.25, -30)
            self.animation.setKeyValueAt(0.5, -50)
            self.animation.setKeyValueAt(0.75, -70)
            self.animation.setEndValue(-20)
            self.animation.setLoopCount(3)
            self.animation.setEasingCurve(QEasingCurve.Type.Linear)
            self.animation.start()
            event.accept()

class Ear2Item(QObject):
    clicked = pyqtSignal()
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self._rotation = 20
        self._pixmap = QPixmap(f"../img/Ears2.png").scaled(120, 120, Qt.AspectRatioMode.KeepAspectRatio).transformed(QTransform().rotate(self._rotation))
        
        self.animation = QPropertyAnimation(self, b"rotation")
        self.animation.setDuration(200)

    @pyqtProperty(int)
    def rotation(self):
        return self._rotation
    
    @rotation.setter
    def rotation(self, value):
        self._rotation = value
        transform = QTransform()
        transform.rotate(self._rotation)
        self._rotated_pixmap = self._pixmap.transformed(transform)
        if self.parent:
            self.parent.update()

    def boundingRect(self):
        return QRectF(-72, -0.2*self._pixmap.height(),
                      3.2*self._pixmap.width(), 1.3*self._pixmap.height())

    def paint(self, painter, option, widget):
        
         # 设置旋转原点为 QPixmap 的左下角
        painter.translate(self._pixmap.width() / 2 + 30, self._pixmap.height())
        painter.rotate(self._rotation)
        painter.drawPixmap(-self._pixmap.width() / 2, -self._pixmap.height(), self._pixmap)

       
    
    def mousePressEvent(self, event):
        
        if event.button() == Qt.MouseButton.LeftButton:
            self.is_follow_mouse = True
            
            self.animation.setStartValue(20)
            self.animation.setKeyValueAt(0.25, 30)
            self.animation.setKeyValueAt(0.75, 70)
            self.animation.setEndValue(20)
            self.animation.setLoopCount(3)
            self.animation.setEasingCurve(QEasingCurve.Type.Linear)
            self.animation.start()
            event.accept()

class EarGraphicsItem(QGraphicsItem):
    def __init__(self, ear_item, parent=None):
        super().__init__(parent)
        self.ear_item = ear_item
        self.ear_item.parent = self
        self.setAcceptHoverEvents(True)
        self.setAcceptedMouseButtons(Qt.MouseButton.LeftButton)
        self.ear_item.clicked.connect(self.handle_ear_click)

    def boundingRect(self):
        return self.ear_item.boundingRect()

    def paint(self, painter, option, widget):
        self.ear_item.paint(painter, option, widget)

    def mousePressEvent(self, event: QMouseEvent):
        self.ear_item.mousePressEvent(event)
        super().mousePressEvent(event)

    def handle_ear_click(self):
        print("Ear clicked!")

    def mouseReleaseEvent(self, event: QMouseEvent):
        self.ear_item.mouseReleaseEvent(event)
        super().mouseReleaseEvent(event)


class EyeItem(QObject):
    clicked = pyqtSignal()  # Add the clicked signal

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self._scale = 1
        self._scaled_pixmap = None
        self._pixmap = QPixmap(f"../img/BasicEyes02.png").scaled(70, 70, Qt.AspectRatioMode.KeepAspectRatio)
        self.animation = QPropertyAnimation(self, b"scaling")
        self.animation.setDuration(500)
        
    @pyqtProperty(float)
    def scaling(self):
        return self._scale
    
    @scaling.setter
    def scaling(self, value):
        self._scale = value
        transform = QTransform()
        transform.scale(1,self._scale)
        self._scaled_pixmap = self._pixmap.transformed(transform)
        if self.parent:
            self.parent.update()

    def boundingRect(self):
        return QRectF(0, -self._pixmap.height(), self._pixmap.width(), self._pixmap.height())

    def paint(self, painter, option, widget):
        if self._scaled_pixmap:
            painter.save()
            
            
            painter.drawPixmap(0, -self._scaled_pixmap.height(), self._scaled_pixmap)
            painter.restore()
        else:
            
            painter.drawPixmap(0, -self._pixmap.height(), self._pixmap)
            
    
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            
            self.clicked.emit()  # Emit the clicked signal
            self.animation.setStartValue(1)
            self.animation.setKeyValueAt(0.25, 0.5)
            self.animation.setKeyValueAt(0.5, 0)
            self.animation.setKeyValueAt(0.75, 0.5)
            self.animation.setEndValue(1)
            self.animation.setLoopCount(3)
            self.animation.setEasingCurve(QEasingCurve.Type.Linear)
            self.animation.start()
            event.accept()

class EyeGraphicsItem(QGraphicsItem):
    def __init__(self, eye_item, parent=None):
        super().__init__(parent)
        self.eye_item = eye_item
        self.eye_item.parent = self
        self.setAcceptHoverEvents(True)
        self.setAcceptedMouseButtons(Qt.MouseButton.LeftButton)
        self.ear_item.clicked.connect(self.handle_ear_click)

    def boundingRect(self):
        return self.eye_item.boundingRect()

    def paint(self, painter, option, widget):
        self.eye_item.paint(painter, option, widget)

    def mousePressEvent(self, event: QMouseEvent):
        self.eye_item.mousePressEvent(event)
        super().mousePressEvent(event)

    def handle_ear_click(self):
        print("Eye clicked!")

    def mouseReleaseEvent(self, event: QMouseEvent):
        self.ear_item.mouseReleaseEvent(event)
        super().mouseReleaseEvent(event)