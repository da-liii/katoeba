import sys
from PyQt4.QtGui import QMainWindow, QHeaderView, QAction
from PyQt4 import QtSql,QtCore
from ui_mainwindow import *
import connection
import sentence as st

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
        self.ui.goButton.clicked.connect(self.insertByRegrex)
        self.ui.comboBox.currentIndexChanged.connect(self.insertByRegrex)

    def insertRecord(self, sentence):
        try:
            iid, lang, st = sentence.split("\t")
            record = QtSql.QSqlRecord()
            if len(st) <= 2:
                print "len <= 2"
            else:
                print st
            f0 = QtSql.QSqlField("stid", QtCore.QVariant.Int)
            f1 = QtSql.QSqlField("tatoid", QtCore.QVariant.Int)
            f2 = QtSql.QSqlField("listid", QtCore.QVariant.Int)
            f3 = QtSql.QSqlField("sentence", QtCore.QVariant.String)
            f4 = QtSql.QSqlField("lang", QtCore.QVariant.String)
            listid = 1
            f0.clear()
            f1.setValue(QtCore.QVariant(iid))
            f2.setValue(QtCore.QVariant(listid))
            f3.setValue(QtCore.QVariant(st))
            f4.setValue(QtCore.QVariant(lang))
            record.append(f0)
            record.append(f1)
            record.append(f2)
            record.append(f3)
            record.append(f4)
            self.model.insertRecord(-1, record)
            self.adjustHeader()
        except ValueError:
            print "an invalid sentence, we ignore it"

    def insertById(self):
        id = self.ui.comboBox.currentText().toInt()
        if id[1]:
            sentence = st.getSentenceById(id[0])
        else:
            return
        self.insertRecord(sentence)

    def insertByRegrex(self):
        regex = self.ui.comboBox.currentText();
        if regex[1]:
            sentences = st.getSentencesByRegex(regex)
        else:
            return
        for sentence in sentences.split("\n"):
            self.insertRecord(sentence)

    def insertByRegrexTemp(self):
        print self.model.insertRow(1,QtCore.QModelIndex())
        

    def initializeModel(self):
        self.model.setTable('sentences')
        self.model.setRelation(2, QtSql.QSqlRelation("list","id","name"))

        self.model.setEditStrategy(QtSql.QSqlTableModel.OnRowChange)
        self.model.select()
        self.model.setHeaderData(1, QtCore.Qt.Horizontal, "ID")
        self.model.setHeaderData(2, QtCore.Qt.Horizontal, "List")
        self.model.setHeaderData(3, QtCore.Qt.Horizontal, "Sentence")
        self.model.setHeaderData(4, QtCore.Qt.Horizontal, "Language")


    def createTableView(self):
        view = self.ui.tableView
        view.setModel(self.model)
        view.setShowGrid(False)
        view.verticalHeader().hide()
        view.setAlternatingRowColors(True)
        view.hideColumn(0)
        return view

    def createListView(self):
        list = self.ui.listView
        list.setModel(self.model.relationModel(2))
        list.setModelColumn(1)
        list.setAlternatingRowColors(True)
        return list

    def adjustHeader(self):
        self.table.horizontalHeader().setResizeMode(3, QHeaderView.Stretch);
        self.table.resizeColumnToContents(1);

    def createMenuBar(self):
        deleteAction = QAction(self.tr("&Delete Sentence..."), self);	
        deleteListAction = QAction(self.tr("&Delete List..."), self);
        quitAction = QAction(self.tr("&Quit"), self);
        aboutAction = QAction(self.tr("&About"), self);
        gotoTatoebaAction = QAction(self.tr("&Go to Tatoeba"), self);
        preferenceAction = QAction(self.tr("&Preference"), self);

        deleteAction.setShortcut(self.tr("Ctrl+D"));
        quitAction.setShortcuts(QtGui.QKeySequence.Quit);

        listMenu = self.ui.menubar.addMenu(self.tr("&Lists"));
        listMenu.addAction(deleteListAction);
        listMenu.addSeparator();
        listMenu.addAction(preferenceAction);
        listMenu.addSeparator();
        listMenu.addAction(quitAction);

        stMenu = self.ui.menubar.addMenu(self.tr("&Sentence"));
        stMenu.addAction(deleteAction);
        stMenu.addAction(gotoTatoebaAction)
    
        helpMenu = self.ui.menubar.addMenu(self.tr("&Help"));
        helpMenu.addAction(aboutAction);
