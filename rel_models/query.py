#!/usr/bin/python


"""
-------------------------------------------------------------------------------
About: Class for a query 
Author: Guanyu Wang
Date: 3-24-2016
-------------------------------------------------------------------------------
"""

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

