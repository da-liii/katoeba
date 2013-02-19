import time
import re
import urllib2
from PyQt4 import QtCore

class Downloader(QtCore.QThread):
    def __init__(self, num):
        super(Downloader, self).__init__()
        self.number = num

    def run(self):
        page = self.getList(self.number)
        self.emit(QtCore.SIGNAL("output(PyQt_PyObject)"), page)

    def getList(self, number):
        url = "http://tatoeba.org/eng/sentences_lists/show/" + number
        content = urllib2.urlopen(url).read()
        spage = re.findall(r'page:\d+', content)
        try:
            npage = int(re.findall(r'\d+', spage[-1])[-1])
        except IndexError:
            npage = 1

        page = []
        result = re.findall(r'sentences_group_\d+', content)
        for each in result:
            page.append(int(re.findall(r'\d+', each)[-1]))
        for i in range(2, npage+1, 1):
            lurl = url + "/page:" + str(i)
            print lurl
            time.sleep(4)
            content = urllib2.urlopen(lurl).read()
            result = re.findall(r'sentences_group_\d+', content)  
            for each in result:
                page.append(int(re.findall(r'\d+', each)[-1]))
            print page
        return page
