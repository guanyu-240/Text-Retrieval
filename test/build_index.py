"""
-------------------------------------------------------------------------------
About: Build inverted index
Author: Guanyu Wang
Date: 3-25-2016
-------------------------------------------------------------------------------
"""
import sys
import json
sys.path.append("../stemming-1.0")
sys.path.append("../")
from stemming.porter2 import stem
from rel_models.db_engine import DB_Session
from doc_process import process

db_s = DB_Session()

dict_terms = {}

freader = open('stop_words')
stop_words = freader.read().split()

docwriter = open('docs.all', 'w') 

def add_to_dict(words, doc_id, doc_len):
  dict_words = {}
  for word in words:
    tmp = dict_words.get(word)
    if tmp == None:
    	tmp = 0
    dict_words[word] = tmp + 1
  termsCountStr = ""
  for k,v in dict_words.iteritems():
        # update list
    temp = dict_terms.get(k)
    if temp == None:
    	temp = [v, 1, doc_id, v]
    else:
    	temp[0] = temp[0] + v
    	temp[1] = temp[1] + 1
    	tmp2 = [doc_id, v]
    	temp = temp + tmp2
    dict_terms[k] = temp
    if len(termsCountStr) > 0:
      termsCountStr += ' '
    termsCountStr += '%s %d' % (k, v)
  docStr = "%s\t#\t%d\t%s\n" % (doc_id, doc_len, termsCountStr)
  db_s.addDocument(doc_id, "#", doc_len, termsCountStr)
  docwriter.write(docStr)



avg_len = 0
freader = open('cacm.all')
line = freader.readline()
catg = ''
doc_id = 0
terms = []
while line != None:
  line = line[:-1]
  if line.startswith('.I'):
    if len(terms) != 0:
    	terms = process(terms, stop_words)
    	#print 'a' in terms
    	#print terms
    	doc_len = len(terms)
    	avg_len += doc_len
    	add_to_dict(terms, doc_id, doc_len)
    words = line.split();
    doc_id = int(words[1])
    if doc_id > 3204:
    	break
    #print "Indexing document " + words[1]
    catg = ''
    terms = []
  elif line.startswith('.'):
    catg = line
  elif catg == '.T' or catg == '.W' or catg == '.K' or catg == '.A':
    words = line.split();
    terms = terms + words
  else: 
    line = freader.readline()
    continue
  line = freader.readline()

total_len = avg_len
avg_len = total_len/3204
print 'num terms:' + str(total_len)
print 'num_unique_terms:' + str(len(dict_terms))
print 'avg_len:' + str(avg_len)

fwriter = open('corpus_info', 'w')
tmp = str(total_len) + ' ' + str(len(dict_terms)) + ' ' + str(avg_len)
fwriter.write(tmp)
fwriter.close()

fwriter = open('index', 'w')
for k,v in dict_terms.iteritems():
  tmp_str = k
  docs_cnt = [str(x) for x in v[2:]]
  docs_cnt_str = ','.join(docs_cnt)
  db_s.addIIEntry(k, float(v[0]), float(v[1]), docs_cnt_str)
  fwriter.write(docs_cnt_str+"\n")

db_s.commit()

fwriter.close()

