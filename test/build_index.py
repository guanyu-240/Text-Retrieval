"""
-------------------------------------------------------------------------------
About: Build inverted index
Author: Guanyu Wang
Date: 3-25-2016
-------------------------------------------------------------------------------
"""
import sys
sys.path.append("../stemming-1.0")
from stemming.porter2 import stem

dict_terms = {}

def char_valid(c):
  if c >= '0' and c <= '9':
    return True
  elif c >= 'A' and c <= 'Z':
    return True
  elif c >= 'a' and c <= 'z':
    return True
  else: return False
  
def remove_white(ls):
  tmp = ls
  for word in tmp:
    if word == '':
    	tmp.remove('')
  return tmp
    
def process(words):
  terms = words
  #print terms
  terms = remove_white(terms)
  for n in range(len(terms)):
    temp = terms[n]
    terms[n] = temp.lower()
  for n in range(len(terms)):
    temp = terms[n]
    #print temp
    first = temp[0]
    if char_valid(first) == False:
    	temp = temp[1:]
    	terms[n] = temp 
  #print terms
  terms = remove_white(terms)
  #print terms
  for n in range(len(terms)):
    temp = terms[n]
    last = temp[-1]
    if char_valid(last) == False:
    	temp = temp[:-1]
    	terms[n] = temp

  terms = remove_white(terms)
  return terms

freader = open('stop_words')
stop_words = freader.read().split()
def stop(words):
  temp = []
  if '' in stop_words:
    stop_words.remove('')
  for a_word in words:
    if a_word not in stop_words:
    	#print 'filter ' + a_word
    	temp.append(a_word)
  return temp
    
def p_stem(words):
  temp = words
  for n in range(len(temp)):
    a_word = temp[n]
    new_word = stem(a_word)
    temp[n] = new_word
  return temp

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
    	terms = process(terms)
    	terms = process(terms)
    	#print terms
    	terms = stop(terms)
    	terms = p_stem(terms)
    	#print 'a' in terms
    	#print terms
    	doc_len = len(terms)
    	avg_len += doc_len
    	add_to_dict(terms, doc_id, doc_len)
    words = line.split();
    doc_id = int(words[1])
    if doc_id > 3204:
    	break
    print "Indexing document " + words[1]
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
  for ele in v:
    tmp_str = tmp_str + ' ' + str(ele)
  tmp_str = tmp_str + '\n'
  fwriter.write(tmp_str)


fwriter.close()

