from math import log,pow
"""
-------------------------------------------------------------------------------
About: library of Retrieval Models
Author: Guanyu Wang
Date: 3-24-2016
-------------------------------------------------------------------------------
"""

def get_okapi (tf, doc_len, avglen):
    okapi = tf/(tf + 0.5 + 1.5*(doc_len/avglen))
    return okapi

def get_okapi_score(use_idf, total_d, total_q, query, doc, df, avg_len, avg_q_len):
  score = 0.0
  termsInDoc = doc.getTermsCount()
  termsInQuery = query.getTermsCount()
  for term, query_tf in termsInQuery.iteritems():
    tf = termsInDoc.get(term)
    if tf == None: tf = 0
    if use_idf:
      idf = 0
      df_term = df.get(term)
      if df_term != 0: idf = log(float(total_d)/float(df_term), 2)
      idf_query = 1 
    else:
      idf = 1
      idf_query = 1
    temp1 = idf * get_okapi(tf, doc.getDocLen(), avg_len)
    temp2 = idf_query * get_okapi(query_tf, query.getLength(), avg_q_len)
    score += temp1*temp2
  return score  
                 
def laplace_smoothing(query, doc, k):
    score = 0.0
    termsInDoc = doc.getTermsCount()
    termsInQuery = query.getTermsCount()
    doc_len = doc.getDocLen() 
    for term,query_tf in termsInQuery.iteritems():
      tf = termsInDoc.get(term)
      if tf == None: tf = float(0)
      score += log(pow((tf + 1)/(float(doc_len) + float(k)), float(query_tf)))
    return score
