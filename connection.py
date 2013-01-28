from PyQt4 import QtSql, QtGui
import sys
import sentence as st

class Data(object):
    def __init__(self):
        if self.createConnection() == False:
            sys.exit(1)
        self.query = QtSql.QSqlQuery()
        self.query.exec_("create table tatoeba(id int primary key, "
                    "sentence varchar(200), lang varchar(3))")
        self.query.exec_("insert into tatoeba values(1,'nini','eng')")

    def createConnection(self):
        db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName(':memory:')
        if not db.open():
            QtGui.QMessageBox.critical(None, QtGui.qApp.tr("Cannot open database"),
                                       QtGui.qApp.tr("Unable to establish a database connection.\n"
                                                     "This example needs SQLite support. Please read "
                                                     "the Qt SQL driver documentation for information "
                                                     "how to build it.\n\n"
                                                     "Click Cancel to exit."),
                                       QtGui.QMessageBox.Cancel)
            return False
        return True

