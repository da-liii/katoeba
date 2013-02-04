#!/usr/bin/env python
# -*- coding:utf-8 -*-
from PyQt4 import QtCore, QtSql
from subprocess import check_output

parser = "tatoparser"
show_id = "--display-ids"
show_lang = "--display-lang"

class Sentence(QtCore.QThread):
    def __init__(self, ddict, ui, model, rrow, llistid):
        super(Sentence, self).__init__()
        self.dict = ddict
        self.model = model
        self.row = rrow
        self.listid = llistid

    def run(self):
        if self.listid == -1:
            print "cannot get listid, should be an exception"
            return 
        self.insertSentence()

    def insertSentence(self):
        print self.dict
        isTr = 'f'
        key = self.dict.keys()[-1]
        value = self.dict[key]
        if key == '-r':
            lvalue = str('.*' + value.toUtf8() + '.*')
        else:
            lvalue = value
        
        if key == '--is-linked-to':
            isTr = 't'
        sentences = unicode(
            check_output([parser, show_id, show_lang, key, lvalue]),
            'utf-8').rstrip("\n")
        for st in sentences.split("\n"):
            self.insertRecord(st, isTr)
            print "inserted", st


    def insertRecord(self, sentence, isTr):
        iid, lang, st = sentence.split("\t")
        record = QtSql.QSqlRecord()
        f0 = QtSql.QSqlField("stid", QtCore.QVariant.Int)
        f1 = QtSql.QSqlField("tatoid", QtCore.QVariant.Int)
        f2 = QtSql.QSqlField("listid", QtCore.QVariant.Int)
        f3 = QtSql.QSqlField("sentence", QtCore.QVariant.String)
        f4 = QtSql.QSqlField("lang", QtCore.QVariant.String)
        f5 = QtSql.QSqlField("sortid", QtCore.QVariant.Int)
        f6 = QtSql.QSqlField("tr", QtCore.QVariant.String)
        f0.clear()
        f1.setValue(QtCore.QVariant(iid))
        f2.setValue(QtCore.QVariant(self.listid))
        f3.setValue(QtCore.QVariant(st))
        f4.setValue(QtCore.QVariant(lang))
        if self.row == -1:
            f5.setValue(QtCore.QVariant(self.model.rowCount()*10))
        else:
            f5.setValue(QtCore.QVariant(self.row*10+1))
        f6.setValue(QtCore.QVariant(isTr))
        record.append(f0)
        record.append(f1)
        record.append(f2)
        record.append(f3)
        record.append(f4)
        record.append(f5)
        record.append(f6)
        print "bug", self.listid, iid
        self.model.insertRecord(-1, record)
