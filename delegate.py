from PyQt4.QtGui import QStyledItemDelegate, QSpinBox, QPixmap, qApp, QStyle, QLineEdit
from PyQt4.QtCore import QVariant, Qt
from PyQt4 import QtCore, QtGui

class Delegate(QStyledItemDelegate):
    def paint(self, painter, option, index):
        col = index.column()
        if col == 4 or col == 1:
            sstr = index.data().toString()
            if col == 1:
                pixmap = QPixmap(":/img/"+ sstr + ".png").scaled(16, 18)
            else:
                pixmap = QPixmap(":/flag/"+ sstr +".png").scaled(30, 20)
            qApp.style().drawItemPixmap(painter, option.rect, Qt.AlignCenter, QPixmap(pixmap))
        else:
            super(Delegate, self).paint(painter, option, index)

    def createEditor(self, parent, option, index):
        col = index.column()
        if col == 2:
            sbox = QSpinBox(parent)
            sbox.setRange(1,100) # 100 is a magic number
            return sbox
        elif col == 1:
            editor = QLineEdit(parent)
            regExp = QtCore.QRegExp("[tri]")
            editor.setValidator(QtGui.QRegExpValidator(regExp, parent))
            return editor
        else:
            return QLineEdit(parent)


    def setEditorData(self,editor,index):
        col = index.column()
        if col == 2:
            item_var=index.data(Qt.DisplayRole)
            item_str=item_var.toPyObject()
            item_int=int(item_str)
            editor.setValue(item_int)
        else:
            super(Delegate, self).setEditorData(editor, index)

    def setModelData(self, editor, model, index):
        col = index.column()
        if col == 2:
            data_int=editor.value()
            data_var=QVariant(data_int)
            model.setData(index,data_var)
        else:
            super(Delegate, self).setModelData(editor, model, index)
