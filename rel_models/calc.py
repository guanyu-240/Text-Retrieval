from math import log,pow
"""
-------------------------------------------------------------------------------
About: library of Retrieval Models
Author: Guanyu Wang
Date: 3-24-2016
-------------------------------------------------------------------------------
"""

def get_okapi (tf, doc_len, avglen):
  """
  Calculate Okapi score of a term
  """
  okapi = float(tf)/(float(tf) + 0.5 + 1.5*(float(doc_len)/float(avglen)))
  return okapi

def get_okapi_score(use_idf, total_d, total_q, query, doc, df, avg_len, avg_q_len):
  """
  Calcualte Okapi score of a document
  """
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
      idf_query = 1.0
    else:
      idf = 1.0
      idf_query = 1.0
    temp1 = idf * get_okapi(tf, doc.getDocLen(), avg_len)
    temp2 = idf_query * get_okapi(query_tf, query.getLength(), avg_q_len)
    score += temp1*temp2
  return score  
                 
def laplace_smoothing(query, doc, k):
  """
  Query likelyhood relevance calculation with Laplace smoothing
  """
  score = 0.0
  termsInDoc = doc.getTermsCount()
  termsInQuery = query.getTermsCount()
  doc_len = doc.getDocLen() 
  for term,query_tf in termsInQuery.iteritems():
    tf = termsInDoc.get(term)
    if tf == None: tf = 0
    score += log(pow((float(tf) + 1.0)/(float(doc_len) + float(k)), float(query_tf)))
  return score

def jm_smoothing(query, doc, lambda_w, cnt_terms_corpus):
  """
  Query likelyhood relevance calculation with Jelinek-Mercer smoothing
  """
  score = 0.0
  termsInDoc = doc.getTermsCount()
  termsInQuery = query.getTermsCount()
  doc_len = doc.getDocLen()
  for term,query_tf in termsInQuery.iteritems():
    tf = termsInDoc.get(term)
    if tf == None: tf = 0
    score_doc = lambda_w*float(tf)/float(doc_len)
    score_corpus = (1.0-lambda_w)/cnt_terms_corpus
    score += log(pow(score_doc + score_corpus, float(query_tf)))
  return score

def okapi_bm25(query, doc, cnt_docs, avg_len, df, b):
  """
  Relevance with Okapi-BM25 language statistic model
  """
  k1 = 1.2
  k2 = 100.0
  score = 0.0
  termsInDoc = doc.getTermsCount()
  termsInQuery = query.getTermsCount()
  k = k1*((1-b)+b*(float(doc.getDocLen())/float(avg_len)))
  for term,query_tf in termsInQuery.iteritems():
    tmp_score = 1.0
    tf = termsInDoc.get(term)
    if tf == None: continue
    n = df.get(term)
    tmp_score *= (float(cnt_docs)-float(n)+0.5)/(float(n)+0.5)
    tmp_score *= (k1+1.0)*float(tf)/(k+float(tf))
    tmp_score *= (k2+1.0)*float(query_tf)/(k2+float(query_tf))
    score += log(tmp_score)
  return score
