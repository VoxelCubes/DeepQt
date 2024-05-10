from typing import Any

import PySide6.QtWidgets as Qw
import PySide6.QtGui as Qg


class CListWidget(Qw.QListWidget):
    """
    Extends the functionality with custom helpers
    And includes a secondary array for data linked to each item
    """

    def __init__(self, parent=None) -> None:
        Qw.QListWidget.__init__(self, parent)
        self._linked_data = []

    def clear(self) -> None:
        Qw.QListWidget.clear(self)
        self._linked_data.clear()

    def addTextItemLinkedData(self, text: str, data: Any) -> None:
        self.addItem(text)
        self._linked_data.append(data)

    def addIconTextItemLinkedData(self, icon: Qg.QIcon, text: str, data: Any) -> None:
        item = Qw.QListWidgetItem(icon, text)
        self.addItem(item)
        self._linked_data.append(data)

    def setCurrentIndexByLinkedData(self, data: Any) -> None:
        self.setCurrentRow(self._linked_data.index(data))

    def indexLinkedData(self, data: Any) -> int:
        return self._linked_data.index(data)

    def currentLinkedData(self) -> Any:
        if self.currentRow() == -1:
            return None
        return self._linked_data[self.currentRow()]
