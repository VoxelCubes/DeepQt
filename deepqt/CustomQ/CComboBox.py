import PySide6.QtWidgets as Qw


class CComboBox(Qw.QComboBox):
    """
    Extends the functionality with custom helpers
    And includes a secondary array for data linked to each item
    """

    def __init__(self, parent=None) -> None:
        Qw.QComboBox.__init__(self, parent)
        self._linked_data = []

    def clear(self) -> None:
        Qw.QComboBox.clear(self)
        self._linked_data.clear()

    def addTextItemLinkedData(self, text: str, data: any) -> None:
        self.addItem(text)
        self._linked_data.append(data)

    def setCurrentIndexByLinkedData(self, data: any) -> None:
        self.setCurrentIndex(self._linked_data.index(data))

    def indexLinkedData(self, data: any) -> None:
        return self._linked_data.index(data)

    def currentLinkedData(self) -> None:
        try:
            return self._linked_data[self.currentIndex()]
        except IndexError:
            print("No linked data found for current index")
            print("Current index:", self.currentIndex())
            print("Linked data:", self._linked_data)
