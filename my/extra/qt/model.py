from typing import Any, AnyStr, Dict, Iterable, List, Union

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItemModel


def modelColumnCells(model: QStandardItemModel, columnIndex: int) -> Iterable[Any]:
    """Yields cells from chosen column"""
    for i in range(model.rowCount()):
        yield model.data(model.index(i, columnIndex))


def modelRemoveAllRows(model: QStandardItemModel):
    """Removes all rows from model"""
    for i in reversed(range(model.rowCount())):
        model.removeRow(i)


def modelHeaders(model: QStandardItemModel, orientation: Qt.Orientation=Qt.Horizontal) -> Iterable[AnyStr]:
    """Yields model header labels"""
    for i in range(model.columnCount()):
        yield model.headerData(i, orientation)


def modelRowCells(model: QStandardItemModel, rowIndex: int, keepHeaders: bool=False) -> Union[Dict, List]:
    """Returns all cells from chosen row index as list of cells or dictionary of header labels and cell values"""
    if keepHeaders:
        return {
            column: model.data(model.index(rowIndex, columnIndex))
            for columnIndex, column in enumerate(modelHeaders(model))
        }
    else:
        return [
            model.data(model.index(rowIndex, columnIndex))
            for columnIndex in range(model.columnCount())
        ]
