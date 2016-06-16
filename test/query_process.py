from doc_process import process
freader = open('query.text')

queries = {}
line = freader.readline()
query_id = 0
terms = []
catg = ''
while line != None:
  line = line[:-1]
  if line.startswith('.I'):
    if len(terms) != 0:
      terms = process(terms)
      #print terms
      #print 'a' in terms
      a_query = [query_id] + terms
      queries[query_id] = terms
      #print a_query
      
    words = line.split()
    query_id = int(words[1])
    if query_id > 64:
      break
    catg = ''
    terms = []
  elif line.startswith('.'):
    catg = line
  elif catg == '.W' or catg == '.A':
    words = line.split()
    terms = terms + words
  elif catg == '.N':
    words = line.split()
    words = words[1:]
    terms = terms + words
  else:
    line = freader.readline()
    continue;
  line = freader.readline()
  
query_dict={}
#print q_id
q_id = int(q_id)
if q_id >=1 and q_id <= 64:
  query_terms = queries.get(q_id)
else:
  input_query = raw_input("Please enter your query terms, press ENTER to finish:")
  query_terms = input_query.split()
  query_terms = process(query_terms)
  query_terms = process(query_terms)
  query_terms = stop(query_terms)
  query_terms = p_stem(query_terms)
  
  
#print query_terms

q_len = len(query_terms)
#print queries
for a_term in query_terms:
  count = query_dict.get(a_term)
  if count == None:
    count = 0
  query_dict[a_term]=(count + 1)
  
df_q = {}
avg_q_len = 0
for k,v in queries.iteritems():
  avg_q_len = avg_q_len + len(v)
  words_list = []
  for word in v:
    if word not in words_list:
      df = df_q.get(word)
      if df == None:
        df = 0
      df = df + 1
      df_q[word] = df
      words_list.append(word)

avg_q_len = float(avg_q_len)/64.0
