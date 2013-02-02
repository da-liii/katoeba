from PyQt4.QtGui import QTableView, QListView
from PyQt4 import QtCore

class KTableView(QTableView):
    def __init__(self, parent=None):
        super(KTableView, self).__init__(parent)

        self.setDragEnabled(True)
        # self.setViewMode(QtGui.QListView.IconMode)
        # self.setIconSize(QtCore.QSize(60, 60))
        # self.setSpacing(10)
        # self.setAcceptDrops(True)

    def startDrag(self, supportedActions):
        item = self.currentItem()

        mimeData = QtCore.QMimeData()
        mimeData.setData('text/plain', itemData)

        drag = QtGui.QDrag(self)
        drag.setMimeData(mimeData)

        if drag.exec_(QtCore.Qt.MoveAction) == QtCore.Qt.MoveAction:
            self.takeItem(self.row(item))

    def dragMoveEvent(self, event):
        if event.mimeData().hasFormat('text/plain'):
            event.setDropAction(QtCore.Qt.MoveAction)
            event.accept()
        else:
            event.ignore()


class KListView(QListView):
    def __init__(self, parent):
        super(KListView, self).__init__(parent)
        self.setAcceptDrops(True)

    def dragEnterEvent(self, e):
        if e.mimeData().hasFormat('text/plain'):
            e.accept()
        else:
            e.ignore() 

    def dropEvent(self, e):
        print "dropped"
