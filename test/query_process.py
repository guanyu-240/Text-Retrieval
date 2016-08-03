import sys
from doc_process import process
from rel_models.db_engine import DB_Session
from rel_models.QueryInfo import newQueryObj

sys.path.append("..")

freader = open('query.text')

freader_stop = open('stop_words')
stop_words = freader_stop.read().split()

# start processing sample queries
queries = {}
terms_count = {}
line = freader.readline()
query_id = 0
terms = []
catg = ''
while line != None:
  line = line[:-1]
  if line.startswith('.I'):
    if len(terms) != 0:
      terms = process(terms, stop_words)
      a_query = [query_id] + terms
      queries[query_id] = terms
      
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

#print query_terms
def process_query(query_terms, algo):
  q_len = len(query_terms)
  for a_term in query_terms:
    count = terms_count.get(a_term)
    if count == None:
      count = 0
    terms_count[a_term]=(count + 1)

  db = DB_Session()
  q = newQueryObj(query_terms)
  query_info = db.getDocsFromQuery(q, 3204)
  if algo == 'okapi':
    return query_info.getOkapiScores(False, 3204, 1, 35, avg_q_len)
  elif algo == 'okapi_idf':
    return query_info.getOkapiScores(True, 3204, 1, 35, avg_q_len)
  elif algo == 'laplace':
    return query_info.getLaplaceSmoothingScores(9742)
  return []

#print q_id
q_id = int(sys.argv[1])
algo = sys.argv[2]
if q_id >=1 and q_id <= 64:
  query_terms = queries.get(q_id)

else:
  input_query = raw_input("Please enter your query terms, press ENTER to finish:")
  query_terms = input_query.split()
  query_terms = process(query_terms, stop_words)
print process_query(query_terms, algo)
