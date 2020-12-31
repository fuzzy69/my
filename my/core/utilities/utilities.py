from PyQt5.QtWidgets import QAction


def _initRecentFiles(self):
    """Initializes recent files menu/actions"""
    for i in range(self._maxRecentFiles):
        self._recentFilesActions.append(QAction(self))
        self._recentFilesActions[i].triggered.connect(self._openRecentFile)
        if i < len(self._recentFiles):
            if not self._clearRecentFilesAction.isEnabled():
                self._clearRecentFilesAction.setEnabled(True)
            self._recentFilesActions[i].setData(self._recentFiles[i])
            self._recentFilesActions[i].setText(self._recentFiles[i])
            self._recentFilesActions[i].setVisible(True)
        else:
            self._recentFilesActions[i].setVisible(False)
        self._recentFilesAction.addAction(self._recentFilesActions[i])
    self._updateRecentFilesActions()


def _updateRecentFiles(self, filePath: str):
    """Updates recent files menu/actions"""
    # FIXME: Replace list with stack
    if filePath not in self._recentFiles:
        self._recentFiles.insert(0, filePath)
    if len(self._recentFiles) > self._maxRecentFiles:
        self._recentFiles.pop()
    self._updateRecentFilesActions()
    if not self._clearRecentFilesAction.isEnabled():
        self._clearRecentFilesAction.setEnabled(True)


def _updateRecentFilesActions(self):
    """Updates recent files actions"""
    for i in range(self._maxRecentFiles):
        if i < len(self._recentFiles):
            self._recentFilesActions[i].setText(self._recentFiles[i])
            self._recentFilesActions[i].setData(self._recentFiles[i])
            self._recentFilesActions[i].setVisible(True)
        else:
            self._recentFilesActions[i].setVisible(False)
