from PyQt5.QtCore import pyqtSlot, QThread


class Thread(QThread):
    """Thin wrapper around Qt's thread class"""

    activeCount = 0

    def __init__(self):
        QThread.__init__(self)
        self.started.connect(self.increaseActiveCount)
        self.finished.connect(self.decreaseActiveCount)

    @pyqtSlot()
    def increaseActiveCount(self):
        """Increases total count number of threads"""
        Thread.activeCount += 1

    @pyqtSlot()
    def decreaseActiveCount(self):
        """Decreases total count number of threads"""
        Thread.activeCount -= 1
