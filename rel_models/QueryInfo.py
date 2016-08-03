"""
-------------------------------------------------------------------------------
About: Class for a Query Information
Author: Guanyu Wang
Date: 3-24-2016
-------------------------------------------------------------------------------
"""

from Models import Document
from sets import Set
from query import Query
from calc import get_okapi_score

class QueryInfo:
  def __init__(self, query, docs, totalDocs, dfTerms):
    self.__query = query
    self.__docs = docs
    self.__totalDocs = totalDocs
    self.__dfTerms = dfTerms

  def output(self):
    print self.__query.getTermsCount()
    print len(self.__docs)
    docIds = [d.docID for d in self.__docs]
    print docIds
    print self.__totalDocs
    print self.__dfTerms

  def getOkapiScores(self, use_idf, total_d, total_q, avg_len, avg_q_len):
    scores = [] 
    for d in self.__docs:
      score = get_okapi_score(use_idf, total_d, total_q, self.__query, d, self.__dfTerms, avg_len, avg_q_len)
      scores.append((d.docID, score))
    scores.sort(key=lambda x: x[1], reverse=True)
    return scores

  def getLaplaceSmoothingScore(self, k):
    scores = []
    for d in self.__docs:
      score = laplace_smoothing(self.__query, d, k)
      scores.append((d.docID, score))
    scores.sort(key=lambda x: x[1], reverse=True)
    return scores
    

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
    cnt = termsCount.get(term)
    if cnt is None:
      termsCount[term] = 1
    else: termsCount[term] = cnt+1
  query = Query(len(query_terms), termsCount)
  return query

def getDocumentByID(doc_id):
  return Document("", "", 0, {})
