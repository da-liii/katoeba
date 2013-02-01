from PyQt4.QtGui import QStyledItemDelegate, QSpinBox, QPixmap, qApp
from PyQt4.QtCore import QVariant, Qt

class IconDelegate(QStyledItemDelegate):
    def paint(self, painter, option, index):
        lang = index.data().toString()
        pixmap = QPixmap(":/flag/"+ lang +".png").scaled(30, 20)
        qApp.style().drawItemPixmap(painter, option.rect, Qt.AlignCenter, QPixmap(pixmap))
