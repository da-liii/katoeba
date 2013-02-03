import sys
from PyQt4.QtGui import QMainWindow, QHeaderView, QAction, QDesktopServices
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
        self.ui.splitter.setStretchFactor(0, 1)
        self.ui.splitter.setStretchFactor(1, 6)


        self.data = connection.Data()
        self.model = QtSql.QSqlRelationalTableModel(self)
        self.initializeModel()
        self.table = self.createTableView()
        self.list = self.createListView()
        self.createMenuBar()

        # signals and slots
        self.ui.goButton.clicked.connect(self.insertByRegex)
        self.ui.comboBox.currentIndexChanged.connect(self.insertByRegex)

    # involving sentence
    def startInsertById(self, number):
        print "before insert ID"
        index = self.list.selectionModel().currentIndex()
        lrow = index.row()
        pindex = self.model.relationModel(2).index(lrow, 0)
        self.listid, test = pindex.data().toInt()
        if test == False:
            print "insertByRegex failed"
        ddict = {}
        ddict["--has-id"] = str(number)
        self.sen = st.Sentence(ddict)
        self.sen.start()
        QtCore.QObject.connect(self.sen, QtCore.SIGNAL('output(PyQt_PyObject)'), self.insertById)
        self.sen.wait()

    def insertById(self, sentences):
        for sentence in sentences.split("\n"):
            st.insertRecord(self, sentence, self.model,-1, 'f', self.listid)
            print "inserted,",sentence
        self.adjustHeader()

    def insertByRegex(self):
        index = self.list.selectionModel().currentIndex()
        lrow = index.row()
        pindex = self.model.relationModel(2).index(lrow, 0)
        listid, test = pindex.data().toInt()
        if test == False:
            print "insertByRegex failed"
        regex = self.ui.comboBox.currentText();
        if regex[1]:
            sentences = st.getSentencesByRegex(regex)
        else:
            return
        for sentence in sentences.split("\n"):
            st.insertRecord(self, sentence, self.model,-1, 'f', listid)
        self.adjustHeader()

    def insertTrById(self):
        index = self.list.selectionModel().currentIndex()
        lrow = index.row()
        pindex = self.model.relationModel(2).index(lrow, 0)
        listid, test = pindex.data().toInt()
        if test == False:
            print "insertTrById failed"
        selection = self.table.selectionModel().selectedRows(0)
        if len(selection) == 0:
            QtGui.QMessageBox.information(self, self.tr("Go to Tatoeba"),
                                          self.tr("You must select one sentence!"))
        else:
            stIndex = selection[0]
            row = stIndex.row()
            iid = stIndex.sibling(row, 1).data().toString()
            print row
            sentences = st.getTranslationById(iid)
            for sentence in sentences.split("\n"):
                st.insertRecord(self, sentence, self.model, row, 't', listid)
        self.adjustHeader()

    # involving MVC
    def initializeModel(self):
        self.model.setTable('sentences')
        self.model.setRelation(2, QtSql.QSqlRelation("list","id","id"))

        self.model.setEditStrategy(QtSql.QSqlTableModel.OnFieldChange)
        self.model.select()
        self.model.setHeaderData(1, QtCore.Qt.Horizontal, "ID")
        self.model.setHeaderData(2, QtCore.Qt.Horizontal, "List")
        self.model.setHeaderData(3, QtCore.Qt.Horizontal, "Sentence")
        self.model.setHeaderData(4, QtCore.Qt.Horizontal, "Language")

    def createTableView(self):
        view = self.ui.tableView
        view.setModel(self.model)
        view.setShowGrid(False)
        #view.verticalHeader().hide()
        view.setAlternatingRowColors(True)
        view.hideColumn(0)
        view.hideColumn(5)
        view.hideColumn(6)
        view.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows);
        view.setSelectionMode(QtGui.QAbstractItemView.SingleSelection);
        iconDelegate = IconDelegate()
        view.setItemDelegateForColumn(4, iconDelegate)
        return view

    def createListView(self):
        llist = self.ui.listView
        llist.setModel(self.model.relationModel(2))
        llist.setModelColumn(1)
        llist.setAlternatingRowColors(True)
        llist.clicked.connect(self.showList)
        llist.setCurrentIndex(self.model.relationModel(2).index(0,0))
        self.adjustHeader()
        return llist

    def adjustHeader(self):
        self.table.horizontalHeader().setResizeMode(3, QHeaderView.Stretch)
        self.table.resizeColumnToContents(1)
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
        number = str(number.toInt())
        self.downloader = dw.Downloader(number)
        self.downloader.start()
        QtCore.QObject.connect(self.downloader, QtCore.SIGNAL('output(PyQt_PyObject)'), self.downloadList)


    def downloadList(self, nums):
        print nums
        for num in nums:
            print num
            self.startInsertById(num)

    # sentence menu
    def gotoTatoeba(self):
        selection = self.table.selectionModel().selectedRows(0)
        if len(selection) == 0:
            QtGui.QMessageBox.information(self, self.tr("Go to Tatoeba"),
                                          self.tr("You must select one sentence!"))
        else:
            stIndex = selection[0]
            iid = stIndex.sibling(stIndex.row(), 1).data().toString()
            url = QtCore.QUrl("http://tatoeba.org/eng/sentences/show/" + iid)
            QDesktopServices.openUrl(url)

    def deleteSentence(self):
        selection = self.table.selectionModel().selectedRows(0)
        
        if len(selection) == 0:
            QtGui.QMessageBox.information(self, self.tr("Delete Sentence From Table"),
                                          self.tr("You must select one sentence!"))
        else:
            stIndex = selection[0]
            row = stIndex.row()
            self.model.removeRow(row)
            self.adjustHeader()

    def aboutTatoeba(self):
        QDesktopServices.openUrl(QtCore.QUrl("http://tatoeba.org"))
