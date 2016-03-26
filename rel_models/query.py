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

"""
Read a document from a line
line format: <id>[tab]<title>[tab]<length>[tab]<terms count>
"""
def readDoc(s):
  parts = s.split("\t")
  if len(parts) != 4: return None
  docID = parts[0]
  title = parts[1]
  docLen = float(parts[2])
  counts = parts[3].split(" ")
  termsCount = {}
  for i in range(len(counts)/2):
    termsCount[counts[2*i]] = float(counts[2*i+1])
  return Document(docID, title, docLen, termsCount)
