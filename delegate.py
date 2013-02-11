# -*- coding: utf-8 -*-
from PyQt4.QtGui import QStyledItemDelegate, QSpinBox, QPixmap, qApp, QStyle, QLineEdit, QItemDelegate
from PyQt4.QtCore import QVariant, Qt
from PyQt4 import QtCore, QtGui

lang = {}
lang["all"] = "Any"
lang["afr"] = "Afrikaans"
lang["ain"] = "Ainu"
lang["sqi"] = "Albanian"
lang["ara"] = "Arabic"
lang["hye"] = "Armenian"
lang["ast"] = "Asturian"
lang["eus"] = "Basque"
lang["bel"] = "Belarusian"
lang["ben"] = "Bengali"
lang["ber"] = "Berber"
lang["bos"] = "Bosnian"
lang["bre"] = "Breton"
lang["bul"] = "Bulgarian"
lang["yue"] = "Cantonese"
lang["cat"] = "Catalan"
lang["cha"] = "Chamorro"
lang["cmn"] = "Chinese"
lang["hrv"] = "Croatian"
lang["cycl"] = "CycL"
lang["ces"] = "Czech"
lang["dan"] = "Danish"
lang["nld"] = "Dutch"
lang["arz"] = "Egyptian Arabic"
lang["eng"] = "English"
lang["epo"] = "Esperanto"
lang["est"] = "Estonian"
lang["ewe"] = "Ewe"
lang["fao"] = "Faroese"
lang["fin"] = "Finnish"
lang["fra"] = "French"
lang["fry"] = "Frisian"
lang["glg"] = "Galician"
lang["kat"] = "Georgian"
lang["deu"] = "German"
lang["grn"] = "Guarani"
lang["heb"] = "Hebrew"
lang["hin"] = "Hindi"
lang["hun"] = "Hungarian"
lang["isl"] = "Icelandic"
lang["ido"] = "Ido"
lang["ind"] = "Indonesian"
lang["ina"] = "Interlingua"
lang["ile"] = "Interlingue"
lang["acm"] = "Iraqi Arabic"
lang["gle"] = "Irish"
lang["ita"] = "Italian"
lang["jpn"] = "Japanese"
lang["xal"] = "Kalmyk"
lang["kaz"] = "Kazakh"
lang["tlh"] = "Klingon"
lang["kor"] = "Korean"
lang["avk"] = "Kotava"
lang["kur"] = "Kurdish"
lang["ksh"] = "Kölsch"
lang["lld"] = "Ladin"
lang["lad"] = "Ladino"
lang["lat"] = "Latin"
lang["lvs"] = "Latvian"
lang["lzh"] = "Literary Chinese"
lang["lit"] = "Lithuanian"
lang["jbo"] = "Lojban"
lang["nds"] = "Low Saxon"
lang["dsb"] = "Lower Sorbian"
lang["mlg"] = "Malagasy"
lang["zsm"] = "Malay"
lang["mal"] = "Malayalam"
lang["mri"] = "Maori"
lang["mar"] = "Marathi"
lang["ell"] = "Modern Greek"
lang["mon"] = "Mongolian"
lang["nob"] = "Norwegian (Bokmål)"
lang["non"] = "Norwegian (Nynorsk)"
lang["nov"] = "Novial"
lang["oci"] = "Occitan"
lang["orv"] = "Old East Slavic"
lang["ang"] = "Old English"
lang["tpw"] = "Old Tupi"
lang["oss"] = "Ossetian"
lang["pes"] = "Persian"
lang["pms"] = "Piemontese"
lang["pol"] = "Polish"
lang["por"] = "Portuguese"
lang["pnb"] = "Punjabi"
lang["que"] = "Quechua"
lang["qya"] = "Quenya"
lang["ron"] = "Romanian"
lang["roh"] = "Romansh"
lang["rus"] = "Russian"
lang["san"] = "Sanskrit"
lang["gla"] = "Scottish Gaelic"
lang["srp"] = "Serbian"
lang["wuu"] = "Shanghainese"
lang["scn"] = "Sicilian"
lang["sjn"] = "Sindarin"
lang["slk"] = "Slovak"
lang["slv"] = "Slovenian"
lang["spa"] = "Spanish"
lang["swh"] = "Swahili"
lang["swe"] = "Swedish"
lang["tgl"] = "Tagalog"
lang["tgk"] = "Tajik"
lang["tat"] = "Tatar"
lang["tel"] = "Telegu"
lang["nan"] = "Teochew"
lang["tha"] = "Thai"
lang["tpi"] = "Tok Pisin"
lang["toki"] = "Toki Pona"
lang["tur"] = "Turkish"
lang["ukr"] = "Ukrainian"
lang["hsb"] = "Upper Sorbian"
lang["urd"] = "Urdu"
lang["uig"] = "Uyghur"
lang["uzb"] = "Uzbek"
lang["vie"] = "Vietnamese"
lang["vol"] = "Volapük"
lang["cym"] = "Welsh"
lang["xho"] = "Xhosa"
lang["yid"] = "Yiddish"

class ItemDelegate(QItemDelegate):
    def setEditorData(self,editor,index):
        super(Delegate, self).setEditorData(editor, index)

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
