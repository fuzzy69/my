from typing import AnyStr

from PyQt5.QtCore import pyqtSlot, pyqtSignal
from PyQt5.QtWebEngineWidgets import (
    QWebEnginePage,
    QWebEngineView,
    QWebEngineSettings,
)
from PyQt5.QtWidgets import QDesktopWidget, QWidget
try:
    from libs.my.core.defaults import USER_AGENT
except ModuleNotFoundError:
    from core.defaults import USER_AGENT


def centerWindow(self: QWidget):
    """Move the window to center of screen"""
    fg = self.frameGeometry()
    c = QDesktopWidget().availableGeometry().center()
    fg.moveCenter(c)
    self.move(fg.topLeft())


class BrowserPage(QWebEnginePage):
    """Web-engine browser page"""

    def __init__(self, userAgent: AnyStr = USER_AGENT, parent: QWidget = None):
        super().__init__(parent)
        self.profile().setHttpUserAgent(userAgent)
        self.profile().cookieStore().deleteAllCookies()

        self.loadFinished.connect(self._loadFinished)
        self.profile().cookieStore().cookieAdded.connect(self._cookieAdded)

    def _cookieAdded(self, cookie):
        """TBI"""
        name = cookie.name().data().decode("utf-8")
        value = cookie.value().data().decode("utf-8")

    def _loadFinished(self):
        """TBI"""
        pass


class BrowserView(QWebEngineView):
    """Renders HTML pages with JavaScript support"""

    contentReady = pyqtSignal(str)
    contentReady2 = pyqtSignal(str)

    def __init__(self, userAgent: AnyStr, parent: QWidget = None):
        super().__init__(parent)
        self.settings().globalSettings().setAttribute(
            QWebEngineSettings.AutoLoadImages, False
        )
        self.settings().globalSettings().setAttribute(
            QWebEngineSettings.JavascriptEnabled, True
        )
        self.setPage(BrowserPage(userAgent))

        self.loadFinished.connect(self._loadFinished)

    def executeJS(self, script: AnyStr):
        """Executes given script code"""
        self.page().runJavaScript(script, self._onExecutedJS)

    @pyqtSlot(str)
    def _onExecutedJS(self, text: AnyStr):
        """Sends content ready signal on executed script"""
        self.contentReady2.emit(text)

    @pyqtSlot(bool)
    def _loadFinished(self, status: bool):
        """Sets page HTML on finished page load"""
        self.page().toHtml(self._onHtml)

    @pyqtSlot(str)
    def _onHtml(self, text: AnyStr):
        """Sends content ready signal on set page HTML"""
        self.contentReady.emit(text)
