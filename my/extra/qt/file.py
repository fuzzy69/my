from typing import AnyStr, Tuple

from PyQt5.QtCore import QFile, QIODevice, QTextStream


def saveTextFile(filePath: AnyStr, text: AnyStr) -> Tuple[bool, AnyStr]:
    """Saves text to file on given file path and returns pair of True and empty string if succeeded or False and
    error message if failed"""
    ok, message = False, ""
    file = QFile(filePath)
    if not file.open(QIODevice.ReadWrite | QIODevice.Truncate | QIODevice.Text):
        message = file.errorString()
    else:
        textStream = QTextStream(file)
        textStream << text
        ok = True
    file.close()

    return ok, message
