#!/usr/bin/env python
# -*- coding:utf-8 -*-
from subprocess import check_output

parser = "tatoparser"
show_id = "--display-ids"
show_lang = "--display-lang"

def getSentenceById(id):
    sentence = unicode(
        check_output([parser, show_id, show_lang, "--has-id", str(id)]),
        'utf-8')
    return sentence

def getTranslationById(id):
    sentences = unicode(
        check_output([parser, show_id, show_lang, "--is-linked-to", str(id)]), 
        'utf-8')
    return sentences

# support filters 
def getSentencesByRegex(regex):
    regexUTF8 = regex.toUtf8()
    sentences = unicode(
        check_output([parser, show_id, show_lang, "-r", str(regexUTF8)]),
        'utf-8')
    return sentences

if __name__=="__main__":
    hello = ".*我们.*"
    getSentencesByRegex(hello)
