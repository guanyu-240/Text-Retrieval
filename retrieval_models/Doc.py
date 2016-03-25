#!/usr/bin/python


"""
-------------------------------------------------------------------------------
About: Class for a document
Author: Guanyu Wang
Date: 3-24-2016
-------------------------------------------------------------------------------
"""

class Document:
  def __init__(self, docID, title, docLen, termsCount):
    self.__docID = docID
    self.__title = title
    self.__docLen = docLen
    self.__termsCount = termsCount

  """
  Getters
  """
  def getID(self):
    return self.__docID
  def getTitle(self):
    return self.__title
  def getDocLen(self):
    return self.__docLen
  def getTermsCount(self):
    return self.__termsCount


class Query:
  def __init__(self, length, termsCount):
    self.__length = length
    self.__termsCount = termsCount

  """
  Getters
  """
  def getLength(self):
    return self.__length
  def getTermsCount(self):
    return self.__termsCount

