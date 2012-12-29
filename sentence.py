#!/usr/bin/env python
# -*- coding:utf-8 -*-
from subprocess import check_output
def getById(id):
    sentence = unicode(check_output(["tatoparser","--has-id", str(id)]),'utf-8')
    return sentence
    
    
