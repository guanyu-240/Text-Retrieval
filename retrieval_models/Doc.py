#!/usr/bin/python


"""
-------------------------------------------------------------------------------
About: Class for a document
Author: Guanyu Wang
Date: 3-24-2016
-------------------------------------------------------------------------------
"""

class Document:
  def __init__(self, docID, title, docLen, wordsCount):
    self.__docID = docID
    self.__title = title
    self.__docLen = docLen
    self.__wordsCount = wordsCount

  """
  Getters
  """
  def getID(self):
    return self.__docID
  def getTitle(self):
    return self.__title
  def getDocLen(self):
    return self.__docLen
  def getWordsCount(self):
    return self.__wordsCount
