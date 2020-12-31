from PyQt5.QtCore import Qt, QPoint, QRect
from PyQt5.QtWidgets import QDesktopWidget, QWidget, QStyle


def moveWindowToCenter(self: QWidget):
    """Moves the window to center of screen"""
    fg = self.frameGeometry()
    c = QDesktopWidget().availableGeometry().center()
    fg.moveCenter(c)
    self.move(fg.topLeft())


def moveWindowToParentCenter(self: QWidget):
    """Moves the window to parent center"""
    parentPosition = self.parentWidget().mapToGlobal(QPoint(0, 0))
    parentRect = QRect(parentPosition, self.parentWidget().size())
    self.move(
        QStyle.alignedRect(
            Qt.LeftToRight, Qt.AlignCenter, self.size(), parentRect
        ).topLeft()
    )
