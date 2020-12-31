from PyQt5.QtCore import pyqtSignal, pyqtSlot, QObject


class WorkerError(Exception):
    """Worker error class"""

    pass


class WorkerStopError(Exception):
    """Worker stop error class"""

    pass


class Worker(QObject):
    """Worker class for background/thread tasks"""

    start = pyqtSignal()
    result = pyqtSignal(dict)
    finished = pyqtSignal(int)
    log = pyqtSignal(int, int, str)

    stopped = pyqtSignal()

    def __init__(self, *args, **kwargs):
        QObject.__init__(self)
        self.__args = args
        self.__kwargs = kwargs
        self._running = True
        self.start.connect(self._onStart)
        self._workerId = 0

    @property
    def isRunning(self) -> bool:
        """Returns True if worker is active"""
        return self._running

    @pyqtSlot()
    def _onStart(self):
        """Runs the worker task"""
        self.doWork(*self.__args, **self.__kwargs)

    @pyqtSlot()
    def _onStop(self):
        """Called on worker's stop signal"""
        self._running = False

    @pyqtSlot()
    def stop(self):
        """Stops the worker"""
        self._running = False

    def doWork(self, *args, **kwargs):
        """Inherit and override this method with the worker task implementation"""
        raise NotImplementedError
