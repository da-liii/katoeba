import shelve
from PyQt4.QtGui import QDialog
from ui_preference import *
# keep these users, for future usage
# config["user"] = []
# block these users, for future usage
# config["buser"] = []
config = shelve.open("config.shelf")
cdict = {}
cdict["trmode"] = {0:"--is-linked-to", 1:"-t",
                   "--is-linked-to":0, "-t":1}
cdict["regex"] = {0:"-r", 1:"-p",
                  "-r":0, "-p":1}
cdict["rmode"] = {0:"easy", 1:"expert",
                  "easy":0, "expert":1}

class Preference(QDialog):
    def __init__(self, parent):
        super(Preference, self).__init__()
        self.pparent = parent
        self.uip = Ui_Dialog()
        self.uip.setupUi(self)
        self.uip.trmodeBox.addItem("Direct Translations")
        self.uip.trmodeBox.addItem("Indirect Links")
        self.uip.regexBox.addItem("Matches the source")
        self.uip.regexBox.addItem("Matches the translations")
        self.uip.rmodeBox.addItem("Easy Mode(.*input.*)")
        self.uip.rmodeBox.addItem("Expert Mode")
        if len(config) == 0:
            self.uip.langEdit.setText("cmn,epo")
            config["lang"] = ["cmn","epo"]
            config["trmode"] = "--is-linked-to"
            config["regex"] = "-r"
            config["rmode"] = "easy"
            config["from"] = 0
            config["to"] = 0
        else:
            self.uip.trmodeBox.setCurrentIndex(cdict["trmode"][config["trmode"]])
            self.uip.regexBox.setCurrentIndex(cdict["regex"][config["regex"]])
            self.uip.rmodeBox.setCurrentIndex(cdict["rmode"][config["rmode"]])
            self.uip.langEdit.setText(",".join(config["lang"]))

    def accept(self):
        config["lang"] = self.uip.langEdit.text().toUtf8().__str__().split(",")
        self.pparent.ui.fromBox.clear()
        self.pparent.ui.toBox.clear()
        self.pparent.ui.fromBox.addItem("all")
        self.pparent.ui.toBox.addItem("all")
        for d in config["lang"]:
            self.pparent.ui.fromBox.addItem(d)
            self.pparent.ui.toBox.addItem(d)
        config["trmode"] = cdict["trmode"][self.uip.trmodeBox.currentIndex()]
        config["regex"] = cdict["regex"][self.uip.regexBox.currentIndex()]
        config["rmode"] = cdict["rmode"][self.uip.rmodeBox.currentIndex()]
        print config
        self.close()
