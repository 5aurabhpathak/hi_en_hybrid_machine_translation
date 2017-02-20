#!/bin/env python3
#Author: Saurabh Pathak
'''this module performs the first stage of the translation system'''
class Ebmt:
    '''Handler class for EBMT - translation unit is a sentence.'''

    def __init__(self, metric=cosine, db):
        self.__metric = metric
        #read into memory all at once to avoid repititive disk access
        with open(db+'.hi') as f, open(db+'.en') as e: self.__f, self.__e = f.read(), e.read()

    def match(self, sent):
        '''returns matched examples'''

