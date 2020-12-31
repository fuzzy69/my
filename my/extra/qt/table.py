from typing import AnyStr, Dict, Iterable, Tuple

from PyQt5.Qt import Qt, QUrl
from PyQt5.QtCore import QObject, pyqtSlot, QModelIndex, QPoint
from PyQt5.QtGui import QDesktopServices, QStandardItem, QStandardItemModel, QBrush
from PyQt5.QtWidgets import QMenu, QTableView, QWidget, QAbstractItemView


def resizeTableViewColumns(tableView: QTableView, columnRatios: Iterable):
    """Resize table-view columns according to given column ratio which should be 1 or less in sum"""
    for i, columnRatio in enumerate(columnRatios):
        if i < tableView.model().columnCount() and isinstance(
            columnRatio, (int, float)
        ):
            tableView.setColumnWidth(i, tableView.frameGeometry().width() * columnRatio)


def setRowBackgroundColor(model: QStandardItemModel, rowIndex: int, color: Qt):
    """
    Sets table row background color
    :param int row: table row index
    :param Qt color: new row background color
    """
    for col in range(model.columnCount()):
        model.setData(model.index(rowIndex, col), QBrush(color), Qt.BackgroundRole)


class Table(QObject):
    """Will be deprecated soon"""

    def __init__(self, parent: QWidget, name: AnyStr, columns: Tuple):
        super().__init__(parent)
        self._name = name
        self._columns = columns
        self._model = QStandardItemModel()
        # self._model = PandasModel(self._columns)
        self._model.setHorizontalHeaderLabels(self._columns)
        self._tableView = QTableView(parent)
        self._tableView.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self._tableView.setSelectionBehavior(QAbstractItemView.SelectRows)
        self._tableView.setSelectionMode(QAbstractItemView.SingleSelection)
        self._tableView.setModel(self._model)
        self._tableView.horizontalHeader().setStretchLastSection(True)
        self._tableView.doubleClicked.connect(self._onDoubleClick)
        self._tableView.setContextMenuPolicy(Qt.CustomContextMenu)
        self._tableView.customContextMenuRequested.connect(self._customContextMenu)
        # self._tableView.contextMenuEvent = self._contextMenuEvent

    @property
    def columns(self) -> list:
        """"""
        return [
            str(self._model.headerData(i, Qt.Horizontal))
            for i in range(self._model.columnCount())
        ]

    @property
    def rowCount(self) -> int:
        """"""
        return self._model.rowCount()

    @property
    def name(self) -> str:
        """"""
        return self._name

    @name.setter
    def name(self, value: str):
        """"""
        self._name = value

    @property
    def model(self) -> QStandardItemModel:
        """"""
        return self._model

    @property
    def tableView(self) -> QTableView:
        """"""
        return self._tableView

    @property
    def view(self) -> QTableView:
        """"""
        return self._tableView

    def setRowCell(self, rowIndex: int, columnIndex: int, data: str):
        """"""
        modelIndex = self._model.index(rowIndex, columnIndex)
        self._model.setData(modelIndex, data)

    def appendRow(self, row: Iterable):
        """"""
        # data = {}
        # for idx, cell in enumerate(row):
        #     data[self._columns[idx]] = cell
        # self._model._data.append(data, ignore_index=True)
        # self._model.dataChanged.emit(0, 0, ())
        self._model.appendRow([QStandardItem(str(item)) for item in row])

    def removeRow(self, rowIndex: int):
        """"""
        self._model.removeRow(rowIndex)

    def removeAllRows(self):
        """"""
        for i in reversed(range(self._model.rowCount())):
            self._model.removeRow(i)

    def columnToList(self, columnIndex: int, reverse: bool = False) -> list:
        """"""
        rowIndexes = (
            range(self._model.rowCount() - 1, -1, -1)
            if reverse
            else range(self._model.rowCount())
        )
        for rowIndex in rowIndexes:
            yield self._model.data(self._model.index(rowIndex, columnIndex))

    def getRow(self, rowIndex: int) -> list:
        """"""
        return [
            self._model.data(self._model.index(rowIndex, columnIndex))
            for columnIndex in range(len(self._columns))
        ]

    def getRowAsDict(self, rowIndex: int) -> Dict:
        """"""
        return {
            column: self._model.data(self._model.index(rowIndex, columnIndex))
            for columnIndex, column in enumerate(self._columns)
        }

    def resizeColumns(self, columnRatios: Iterable):
        """"""
        for i, columnRatio in enumerate(columnRatios):
            if i < self._model.columnCount() and isinstance(columnRatio, (int, float)):
                # print(self._tableView.frameGeometry().width())
                self._tableView.setColumnWidth(
                    i, self._tableView.frameGeometry().width() * columnRatio
                )

    # def selectedRows(self) -> list:
    def selectedRows(self) -> set:
        """"""
        return set(
            [
                index.row()
                for index in self._tableView.selectionModel().selectedIndexes()
            ]
        )

    def selectedRowsCount(self) -> int:
        """"""
        return len(self.selectedRows())

    def selectAll(self):
        self.tableView.selectAll()

    def selectNone(self):
        self.tableView.clearSelection()

    def invertSelection(self):
        rowIndexes = self.selectedRows()
        self.selectNone()
        for rowIndex in range(self.model.rowCount()):
            if rowIndex not in rowIndexes:
                self.tableView.selectRow(rowIndex)

    @pyqtSlot()
    def test(self):
        """"""
        print("Test slot")

    @pyqtSlot(QModelIndex)
    def _onDoubleClick(self, modelIndex: QModelIndex):
        """
        Opens the double clicked row's URL in a default browser
        :param QModelIndex modelIndex: table model index
        """
        if "URL" in self._columns:
            index = self._columns.index("URL")
            model = modelIndex.model()
            url = QUrl(model.data(model.index(modelIndex.row(), index)))
            QDesktopServices.openUrl(url)

    def _customContextMenu(self, pos: QPoint):
        """"""
        modelIndex = self._tableView.indexAt(pos)
        menu = QMenu()
        a1Action = menu.addAction("Open add in browser")
        a2Action = menu.addAction("Open seller profile in browser")
        action = menu.exec_(self._tableView.viewport().mapToGlobal(pos))
        if action == a1Action:
            url = QUrl(
                self._model.data(
                    self._model.index(modelIndex.row(), self._columns.index("URL"))
                )
            )
        elif action == a2Action:
            url = QUrl(
                "https://www.facebook.com/profile.php?id="
                + self._model.data(
                    self._model.index(modelIndex.row(), self._columns.index("User ID"))
                )
            )
        else:
            url = None
        if url is not None:
            QDesktopServices.openUrl(url)

    # def _contextMenuEvent(self, event):
    #     menu = QMenu(self)
    #     quitAction = menu.addAction("Quit")
    #     action = menu.exec_(self.mapToGlobal(event.pos()))
    # if action == quitAction:
    #     qApp.quit()

    def setRowBackgroundColor(self, rowIndex: int, color: Qt):
        """
        Sets table row background color
        :param int row: table row index
        :param Qt color: new row background color
        """
        for col in range(self.model.columnCount()):
            self.model.setData(
                self.model.index(rowIndex, col), QBrush(color), Qt.BackgroundRole
            )
