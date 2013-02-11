# -*- coding: utf-8 -*-
import sys
import os
from config import *
from PyQt4.QtGui import QMainWindow, QHeaderView, QAction, QDesktopServices, QFileDialog
from PyQt4 import QtSql,QtCore
from ui_mainwindow import *
from dialog import *
import connection
import sentence as st
import download as dw
from delegate import *
class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.splitter.setStretchFactor(0, 10)
        self.ui.splitter.setStretchFactor(1, 34)
        self.data = connection.Data()
        self.model = QtSql.QSqlRelationalTableModel(self)
        self.initializeModel()
        self.table = self.createTableView()
        self.list = self.createListView()
        self.createMenuBar()

        # signals and slots
        self.ui.goButton.clicked.connect(self.insertByRegex)
        self.ui.comboBox.currentIndexChanged.connect(self.insertByRegex)
        qApp.aboutToQuit.connect(self.beforeQuit)
        self.ui.fromBox.setItemDelegate(ItemDelegate())
        self.ui.toBox.setItemDelegate(ItemDelegate())
        self.ui.fromBox.addItem("all")
        self.ui.toBox.addItem("all")
        for d in config["lang"]:
            self.ui.fromBox.addItem(d)
            self.ui.toBox.addItem(d)
        self.ui.fromBox.setCurrentIndex(config["from"])
        self.ui.toBox.setCurrentIndex(config["to"])

    def beforeQuit(self):
        config["to"] = self.ui.toBox.currentIndex()
        config["from"] = self.ui.fromBox.currentIndex()
        config.close()

    def test(self):
        self.insertById(12)

    def getListId(self):
        index = self.list.selectionModel().currentIndex()
        lrow = index.row()
        pindex = self.model.relationModel(2).index(lrow, 0)
        listid, test = pindex.data().toInt()
        if test:
            return listid
        else:
            return -1

    def getSentenceIndex(self):
        listid = self.getListId()
        selection = self.table.selectionModel().selectedIndexes()
        if len(selection) == 0:
            QtGui.QMessageBox.information(self, self.tr("Which sentence?"),
                                          self.tr("You must select one sentence!"))
            return None
        else:
            return selection[0]

    # involving sentence
    def insertById(self, number):
        listid = self.getListId()
        ddict = {}
        ddict["--has-id"] = str(number)
        sen = st.Sentence(ddict, self.ui, self.model, -1, listid)
        sen.start()
        self.ui.statusbar.showMessage("inserting "+ str(number))
        sen.wait()

    def insertByRegex(self):
        listid = self.getListId()
        regex = self.ui.comboBox.currentText();
        if len(regex) > 1:
            ddict = {}
            if config["rmode"] == "easy":
                ddict[config["regex"]] = str('.*' + regex.toUtf8() + '.*')
            else:
                ddict[config["regex"]] = str(regex.toUtf8())
            ddict["--is-translatable-in"] = self.ui.toBox.currentText()
            ddict["--lang"] = self.ui.fromBox.currentText()
            sen = st.Sentence(ddict, self.ui, self.model, -1, listid)
            sen.start()
            sen.wait()
        else:
            return

    def insertTrById(self):
        listid = self.getListId()
        stIndex = self.getSentenceIndex()
        if stIndex == None:
            return
        row = stIndex.row()
        iid = stIndex.sibling(row, 6).data().toString()
        ddict = {}
        ddict[config["trmode"]] = iid
        ddict["--lang"] = self.ui.toBox.currentText()
        sen = st.Sentence(ddict, self.ui, self.model, row, listid)
        sen.start()
        sen.wait()
        self.filter()

    def insertAllTrById(self):
        listid = self.getListId()
        while self.model.canFetchMore():
            self.model.fetchMore()
        cnt = self.model.rowCount()
        trlist = []
        for i in range(cnt):
            stIndex = self.model.index(i,0)
            row = stIndex.row()
            iid = stIndex.sibling(row, 6).data().toString()
            trlist.append(iid)
        for iid in trlist:
            ddict = {}
            ddict[config["trmode"]] = iid
            ddict["--lang"] = self.ui.toBox.currentText()
            sen = st.Sentence(ddict, self.ui, self.model, row, listid)
            sen.start()
            sen.wait()

    def exportForAnki(self):
        home = os.getenv("HOME", "/home")
        fileName = QFileDialog.getOpenFileName(self,
                                               self.tr("Open File"),
                                               home,
                                               self.tr("Any Files"))
        f = open(fileName, "w")
        while self.model.canFetchMore():
            self.model.fetchMore()
        cnt = self.model.rowCount()
        for i in range(cnt/2):
            stIndex = self.model.index(2*i, 0)
            row = stIndex.row()
            entry = stIndex.sibling(row, 3).data().toString().toUtf8() + "\t"
            stIndex = self.model.index(2*i+1, 0)
            row = stIndex.row()
            entry += stIndex.sibling(row, 3).data().toString().toUtf8() + "\n"
            f.write(entry)
        f.close()

    # involving MVC
    def initializeModel(self):
        self.model.setTable('sentences')
        self.model.setRelation(2, QtSql.QSqlRelation("list","id","id"))

        self.model.setEditStrategy(QtSql.QSqlTableModel.OnFieldChange)
        self.model.select()
        self.model.setHeaderData(1, QtCore.Qt.Horizontal, "ID")
        self.model.setHeaderData(2, QtCore.Qt.Horizontal, "List")
        self.model.setHeaderData(3, QtCore.Qt.Horizontal, "Sentence")
        self.model.setHeaderData(4, QtCore.Qt.Horizontal, "Lang")

    def createTableView(self):
        view = self.ui.tableView
        view.setModel(self.model)
        view.setShowGrid(False)
        #view.verticalHeader().hide()
        view.setAlternatingRowColors(True)
        view.hideColumn(0)
        view.hideColumn(5)
        view.hideColumn(6)
        view.setSelectionBehavior(QtGui.QAbstractItemView.SelectItems);
        view.setSelectionMode(QtGui.QAbstractItemView.SingleSelection);
        view.setItemDelegate(Delegate())
        view.setColumnWidth(1, 20)
        view.setColumnWidth(2, 40)
        view.setColumnWidth(4, 36)
        view.horizontalHeader().setResizeMode(3, QHeaderView.Stretch)
        return view

    def createListView(self):
        llist = self.ui.listView
        llist.setModel(self.model.relationModel(2))
        llist.setModelColumn(1)
        llist.setAlternatingRowColors(True)
        llist.clicked.connect(self.showList)
        llist.setCurrentIndex(self.model.relationModel(2).index(0,0))
        self.filter()
        return llist

    def filter(self):
        self.model.sort(5, QtCore.Qt.AscendingOrder)

    # involving menu entry
    def createMenuBar(self):
        quitAction = QAction(self.tr("&Quit"), self)
        aboutAction = QAction(self.tr("&About"), self)
        aboutTatoebaAction = QAction(self.tr("About Tatoeba"), self)
        preferenceAction = QAction(self.tr("&Preference"), self)

        quitAction.setShortcuts(QtGui.QKeySequence.Quit)

        listMenu = self.ui.menubar.addMenu(self.tr("&Lists"))

        addListAction = QAction(self.tr("&Add List"), self)
        listMenu.addAction(addListAction)
        addListAction.triggered.connect(self.addList)

        deleteListAction = QAction(self.tr("&Delete List"), self)
        listMenu.addAction(deleteListAction)
        deleteListAction.triggered.connect(self.deleteList)

        clearListAction = QAction(self.tr("C&lear List"), self)
        listMenu.addAction(clearListAction)
        clearListAction.setShortcut(self.tr("Ctrl+L"))
        clearListAction.triggered.connect(self.deleteAllSentence)

        insertAllTrAction = QAction(self.tr("Insert All Tranlastions"), self)
        listMenu.addAction(insertAllTrAction)
        insertAllTrAction.triggered.connect(self.insertAllTrById)

        exportAction = QAction(self.tr("Export For Anki"), self)
        listMenu.addAction(exportAction)
        exportAction.triggered.connect(self.exportForAnki)

        downloadListAction = QAction(self.tr("Download List"), self)
        listMenu.addAction(downloadListAction)
        downloadListAction.triggered.connect(self.startDownloadList)

        listMenu.addSeparator()
        listMenu.addAction(preferenceAction)
        listMenu.addSeparator()
        listMenu.addAction(quitAction)

        stMenu = self.ui.menubar.addMenu(self.tr("&Sentences"))
        getTrAction = QAction(self.tr("Get &Translations"), self)
        stMenu.addAction(getTrAction)

        gotoTatoebaAction = QAction(self.tr("&Go to Tatoeba"), self)
        stMenu.addAction(gotoTatoebaAction)
        gotoTatoebaAction.triggered.connect(self.gotoTatoeba)

        deleteAction = QAction(self.tr("&Delete Sentence..."), self)
        stMenu.addAction(deleteAction)
        deleteAction.triggered.connect(self.deleteSentence)

        deleteAction.setShortcut(self.tr("Ctrl+D"))
        gotoTatoebaAction.setShortcut(self.tr("Ctrl+G"))
        getTrAction.setShortcut(self.tr("Ctrl+T"))

        helpMenu = self.ui.menubar.addMenu(self.tr("&Help"))
        helpMenu.addAction(aboutAction)
        helpMenu.addAction(aboutTatoebaAction)

        getTrAction.triggered.connect(self.insertTrById)
        aboutTatoebaAction.triggered.connect(self.aboutTatoeba)

    # list menu
    def showList(self, index):
        row = index.row()
        if row >= 0:
            pindex = self.model.relationModel(2).index(row, 0)
            self.model.setFilter(QtCore.QString("listid = " + pindex.data().toString()))
        else:
            print "unexpected in mainwindow showList"

    def addList(self):
        record = QtSql.QSqlRecord()
        f0 = QtSql.QSqlField("id", QtCore.QVariant.Int)
        f1 = QtSql.QSqlField("name", QtCore.QVariant.String)
        f2 = QtSql.QSqlField("number", QtCore.QVariant.Int)
        f0.clear()
        f1.setValue(QtCore.QVariant("New List"))
        f2.setValue(QtCore.QVariant(0)) # will be used later
        record.append(f0)
        record.append(f1)
        record.append(f2)
        count = self.model.relationModel(2).rowCount()
        self.model.relationModel(2).insertRecord(count, record)
        self.ui.listView.setCurrentIndex(self.model.relationModel(2).index(count,0))
        self.showList(self.ui.listView.currentIndex())

    def deleteAllSentence(self):
        self.model.removeRows(0, self.model.rowCount())

    def deleteList(self):
        index = self.list.selectionModel().currentIndex()
        row = index.row()
        if row >= 0:
            self.deleteAllSentence()
            self.model.relationModel(2).removeRow(row)
        else:
            print "unexpected in mainwindow deleteList"

    def startDownloadList(self):
        dialog = Dialog()
        if dialog.exec_() == 1:
            number = dialog.ui.lineEdit.text()
        else:
            return
        number = str(number.toInt()[0])
        self.downloader = dw.Downloader(number)
        self.downloader.start()
        QtCore.QObject.connect(self.downloader, QtCore.SIGNAL('output(PyQt_PyObject)'), self.downloadList)


    def downloadList(self, nums):
        print nums
        for num in nums:
            print num
            self.insertById(num)

    # sentence menu
    def gotoTatoeba(self):
        stIndex = self.getSentenceIndex()
        if stIndex == None:
            return
        iid = stIndex.sibling(stIndex.row(), 6).data().toString()
        url = QtCore.QUrl("http://tatoeba.org/eng/sentences/show/" + iid)
        QDesktopServices.openUrl(url)

    def deleteSentence(self):
        stIndex = self.getSentenceIndex()
        if stIndex == None:
            return
        row = stIndex.row()
        self.model.removeRow(row)
        self.table.setCurrentIndex(stIndex)

    def aboutTatoeba(self):
        QDesktopServices.openUrl(QtCore.QUrl("http://tatoeba.org"))

