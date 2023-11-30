import sys
from PyQt5.QtCore import Qt, QModelIndex, QAbstractTableModel, QEvent
from PyQt5.QtGui import QStandardItemModel
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QTableView,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QStyledItemDelegate,
)

class ButtonDelegate(QStyledItemDelegate):
    def __init__(self, parent=None):
        super().__init__(parent)

    def paint(self, painter, option, index):
        if index.column() == index.model().columnCount() - 1:
            self.drawButton(painter, option, index)
        else:
            QStyledItemDelegate.paint(self, painter, option, index)

    def drawButton(self, painter, option, index):
        button = QPushButton("Delete", self.parent())
        button.setGeometry(option.rect)
        button.clicked.connect(lambda: self.deleteRow(index))
        button.show()

    def editorEvent(self, event, model, option, index):
        if index.column() == index.model().columnCount() - 1:
            button_rect = option.rect
            if button_rect.contains(event.pos()):
                return True  # Consume the event to prevent default handling

        return QStyledItemDelegate.editorEvent(self, event, model, option, index)

    def deleteRow(self, index):
        model = index.model()
        model.removeRow(index.row())


class CustomTableModel(QAbstractTableModel):
    def __init__(self, data, parent=None):
        super().__init__(parent)
        self._data = data
        self.headers = ['Column 1', 'Column 2', 'Column 3', 'Delete']

    def rowCount(self, parent=QModelIndex()):
        return len(self._data)

    def columnCount(self, parent=QModelIndex()):
        return len(self.headers)

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            row = index.row()
            col = index.column()
            if 0 <= row < len(self._data) and 0 <= col < len(self._data[0]):
                return str(self._data[row][col])
        elif role == Qt.TextAlignmentRole:
            return Qt.AlignCenter

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            return self.headers[section]

    def flags(self, index):
        if index.column() == self.columnCount() - 1:
            return Qt.ItemIsEnabled | Qt.ItemIsSelectable
        else:
            return Qt.ItemFlags(QAbstractTableModel.flags(self, index) | Qt.ItemIsEditable)

    def setData(self, index, value, role=Qt.EditRole):
        if role == Qt.EditRole:
            if index.column() == self.columnCount() - 1:
                return False
            self._data[index.row()][index.column()] = value
            self.dataChanged.emit(index, index)
            return True
        return False

    def removeRow(self, row, parent=QModelIndex()):
        self.beginRemoveRows(parent, row, row)
        del self._data[row]
        self.endRemoveRows()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("QTableView Example")
        self.setGeometry(100, 100, 600, 400)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.table_view = QTableView(self)
        self.central_layout = QVBoxLayout(self.central_widget)
        self.central_layout.addWidget(self.table_view)

        data = [
            ['A1', 'B1', 'C1'],
            ['A2', 'B2', 'C2'],
            ['A3', 'B3', 'C3'],
            ['A4', 'B4', 'C4'],
        ]

        self.model = CustomTableModel(data)
        self.table_view.setModel(self.model)

        self.table_view.setColumnWidth(self.model.columnCount() - 1, 80)

        button_delegate = ButtonDelegate(self.table_view)
        self.table_view.setItemDelegateForColumn(self.model.columnCount() - 1, button_delegate)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
