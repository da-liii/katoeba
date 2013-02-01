import sys
from PyQt4.QtGui import QMainWindow, QHeaderView, QAction, QDesktopServices
from PyQt4 import QtSql,QtCore
from ui_mainwindow import *
import connection
import sentence as st
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
        self.ui.goButton.clicked.connect(self.test)
        self.ui.comboBox.currentIndexChanged.connect(self.insertByRegrex)

    def test(self):
        print self.model.setData(self.model.index(0,1,QtCore.QModelIndex() ), QtGui.QColor("#00ff00"), QtCore.Qt.DecorationRole)
        
    # involving sentence
    def insertByRegrex(self):
        regex = self.ui.comboBox.currentText();
        if regex[1]:
            sentences = st.getSentencesByRegex(regex)
        else:
            return
        for sentence in sentences.split("\n"):
            st.insertRecord(self, sentence, self.model,-1, 'f')
        self.adjustHeader()

    def insertTrById(self):
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
                st.insertRecord(self, sentence, self.model, row, 't')
        self.adjustHeader()

    # involving MVC
    def initializeModel(self):
        self.model.setTable('sentences')
        self.model.setRelation(2, QtSql.QSqlRelation("list","id","name"))

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
        list = self.ui.listView
        list.setModel(self.model.relationModel(2))
        list.setModelColumn(1)
        list.setAlternatingRowColors(True)
        return list

    def adjustHeader(self):
        self.table.horizontalHeader().setResizeMode(3, QHeaderView.Stretch)
        self.table.resizeColumnToContents(1)
        self.model.sort(5, QtCore.Qt.AscendingOrder)


    # involving menu entry
    def createMenuBar(self):
        deleteListAction = QAction(self.tr("&Delete List..."), self)
        quitAction = QAction(self.tr("&Quit"), self)
        aboutAction = QAction(self.tr("&About"), self)
        aboutTatoebaAction = QAction(self.tr("About Tatoeba"), self)
        preferenceAction = QAction(self.tr("&Preference"), self)

        quitAction.setShortcuts(QtGui.QKeySequence.Quit)

        listMenu = self.ui.menubar.addMenu(self.tr("&Lists"))
        listMenu.addAction(deleteListAction)
        listMenu.addSeparator()
        listMenu.addAction(preferenceAction)
        listMenu.addSeparator()
        listMenu.addAction(quitAction)

        stMenu = self.ui.menubar.addMenu(self.tr("&Sentence"))
        getTrAction = QAction(self.tr("Get &Translations"), self)
        stMenu.addAction(getTrAction)
        gotoTatoebaAction = QAction(self.tr("&Go to Tatoeba"), self)
        stMenu.addAction(gotoTatoebaAction)
        deleteAction = QAction(self.tr("&Delete Sentence..."), self)
        stMenu.addAction(deleteAction)

        deleteAction.setShortcut(self.tr("Ctrl+D"))
        gotoTatoebaAction.setShortcut(self.tr("Ctrl+G"))
        getTrAction.setShortcut(self.tr("Ctrl+T"))
    
        helpMenu = self.ui.menubar.addMenu(self.tr("&Help"))
        helpMenu.addAction(aboutAction)
        helpMenu.addAction(aboutTatoebaAction)

        gotoTatoebaAction.triggered.connect(self.gotoTatoeba)
        getTrAction.triggered.connect(self.insertTrById)
        aboutTatoebaAction.triggered.connect(self.aboutTatoeba)

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

    def aboutTatoeba(self):
        QDesktopServices.openUrl(QtCore.QUrl("http://tatoeba.org"))
