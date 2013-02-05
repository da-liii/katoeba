# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui.ui'
#
# Created: Tue Feb  5 16:54:06 2013
#      by: PyQt4 UI code generator 4.9.6
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(664, 417)
        MainWindow.setStyleSheet(_fromUtf8(""))
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setStyleSheet(_fromUtf8(""))
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        self.fromBox = QtGui.QComboBox(self.centralwidget)
        self.fromBox.setObjectName(_fromUtf8("fromBox"))
        self.horizontalLayout.addWidget(self.fromBox)
        self.comboBox = QtGui.QComboBox(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBox.sizePolicy().hasHeightForWidth())
        self.comboBox.setSizePolicy(sizePolicy)
        self.comboBox.setEditable(True)
        self.comboBox.setMinimumContentsLength(3)
        self.comboBox.setObjectName(_fromUtf8("comboBox"))
        self.horizontalLayout.addWidget(self.comboBox)
        self.label_2 = QtGui.QLabel(self.centralwidget)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout.addWidget(self.label_2)
        self.toBox = QtGui.QComboBox(self.centralwidget)
        self.toBox.setObjectName(_fromUtf8("toBox"))
        self.horizontalLayout.addWidget(self.toBox)
        self.goButton = QtGui.QPushButton(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Monospace"))
        font.setPointSize(11)
        self.goButton.setFont(font)
        self.goButton.setStyleSheet(_fromUtf8(""))
        self.goButton.setObjectName(_fromUtf8("goButton"))
        self.horizontalLayout.addWidget(self.goButton)
        self.horizontalLayout.setStretch(0, 2)
        self.horizontalLayout.setStretch(1, 8)
        self.horizontalLayout.setStretch(2, 20)
        self.horizontalLayout.setStretch(3, 2)
        self.horizontalLayout.setStretch(4, 8)
        self.horizontalLayout.setStretch(5, 4)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.splitter = QtGui.QSplitter(self.centralwidget)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setHandleWidth(4)
        self.splitter.setObjectName(_fromUtf8("splitter"))
        self.layoutWidget = QtGui.QWidget(self.splitter)
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.vLayout = QtGui.QVBoxLayout(self.layoutWidget)
        self.vLayout.setSpacing(2)
        self.vLayout.setSizeConstraint(QtGui.QLayout.SetMinimumSize)
        self.vLayout.setMargin(0)
        self.vLayout.setObjectName(_fromUtf8("vLayout"))
        self.listView = QtGui.QListView(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Monospace"))
        font.setPointSize(12)
        self.listView.setFont(font)
        self.listView.setObjectName(_fromUtf8("listView"))
        self.vLayout.addWidget(self.listView)
        self.commandLinkButton = QtGui.QCommandLinkButton(self.layoutWidget)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/image/refresh.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.commandLinkButton.setIcon(icon)
        self.commandLinkButton.setObjectName(_fromUtf8("commandLinkButton"))
        self.vLayout.addWidget(self.commandLinkButton)
        self.tableView = QtGui.QTableView(self.splitter)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Monospace"))
        self.tableView.setFont(font)
        self.tableView.setObjectName(_fromUtf8("tableView"))
        self.verticalLayout.addWidget(self.splitter)
        self.verticalLayout.setStretch(0, 1)
        self.verticalLayout.setStretch(1, 10)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 664, 22))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Monospace"))
        font.setPointSize(9)
        self.menubar.setFont(font)
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.action_About = QtGui.QAction(MainWindow)
        self.action_About.setObjectName(_fromUtf8("action_About"))

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.label.setText(_translate("MainWindow", "From:", None))
        self.label_2.setText(_translate("MainWindow", "To:", None))
        self.goButton.setText(_translate("MainWindow", "Search", None))
        self.commandLinkButton.setText(_translate("MainWindow", "Check for updates", None))
        self.action_About.setText(_translate("MainWindow", "&About", None))

import tatoeba_rc
