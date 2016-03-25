"""
-------------------------------------------------------------------------------
About: Class for a Query Information
Author: Guanyu Wang
Date: 3-24-2016
-------------------------------------------------------------------------------
"""

from Doc import Document
from sets import Set

class QueryInfo:
  def __init__(self, query, totalDocs, df):
    self.__query = query
    self.__docs =
    self.__totalDocs = totalDocs
    self.__df = df


def generateQueryInfo(query, ii_list, totalDocs):
  termsCount = query.getTermsCount()
  if len(termsCount) != len(ii):
    return None
  df = {}
  doc_ids = Set([])
  docs = Set([])
  i = 0
  for term,cnt in termsCount.iterItems():
    if ii_list[i] is None: df.append(0)
    else: df.append(len(ii_list[i]))
    for ele in ii_list[i]:
      if ele[0] not in doc_ids:
        doc_ids.add(ele[0])
        docs.add(getDocumentByID(ele[0]))
    i += 1
  return QueryInfo(query, docs, totalDocs, df)
    

def newQueryObj(query_terms):
  termsCount = {}
  for term in query_terms:
    cnt = termsCount.get(term):
    if cnt is None:
      termsCount[term] = 1
    else: termsCount[term] = cnt+1
  query = Query(len(query_terms), termsCount)
  return query

def getDocumentByID(doc_id):
  return Document("", "", 0, {})
