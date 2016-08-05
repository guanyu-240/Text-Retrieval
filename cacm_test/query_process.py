import sys
from doc_process import process
from rel_models.db_engine import DB_Session
from rel_models.QueryInfo import newQueryObj

sys.path.append("..")

freader = open('query.text')

freader_stop = open('stop_words')
stop_words = freader_stop.read().split()

cnt_terms_corpus = 0
cnt_unique_terms = 0
avg_doc_len = 0

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

def output_query(q_id, scores, algo_name, fw):
  rank = 1
  for score in scores:
    if rank > 1000: break
    line = "%d Q0 CACM-%s %d %f %s\n" % (q_id, score[0], rank, score[1], algo_name)
    rank += 1
    fw.write(line)

def process_single_query(q_id, db, query_terms, algo, fw):
  q_len = len(query_terms)
  q = newQueryObj(query_terms)
  query_info = db.getDocsFromQuery(q, 3204)
  scores = None
  if algo == 'Okapi':
    scores = query_info.getOkapiScores(False, 3204, 1, avg_doc_len, avg_q_len)
  elif algo == 'Okapi_IDF':
    scores = query_info.getOkapiScores(True, 3204, 1, avg_doc_len, avg_q_len)
  elif algo == 'Laplace':
    scores = query_info.getLaplaceSmoothingScore(cnt_unique_terms)
  elif algo == 'JM':
    scores = query_info.getJMSmoothingScore(0.2, cnt_terms_corpus)
  elif algo == 'bm25':
    scores = query_info.getBM25Score(3204, avg_doc_len, 0.75)
  output_query(q_id, scores, algo, fw)

def process_query(q_id, query_terms, algo, f_name):
  fw = open(f_name, "w")
  db = DB_Session()
  if q_id >= 1 and q_id <= 64:
    q_terms = queries[q_id]
    process_single_query(q_id, db, q_terms, algo, fw)
  elif q_id == 0:
    for q_idx in range(1, 65):
      q_terms = queries[q_idx]
      process_single_query(q_idx, db, q_terms, algo, fw)
  else:
    process_single_query(-1, db, query_terms, algo, fw)
  fw.close()
    
#print q_id
if len(sys.argv) < 4:
  print "Usage: %s <query id> <algorithm> <output file>"
  sys.exit(1)

q_id = int(sys.argv[1])
algo = sys.argv[2]
f_name = sys.argv[3]
query_terms = None

corpus_info = open("corpus_info").read().split()
cnt_terms_corpus,cnt_unique_terms,avg_doc_len = int(corpus_info[0]),int(corpus_info[1]),int(corpus_info[2])

if q_id == -1:
  input_query = raw_input("Please enter your query terms, press ENTER to finish:")
  query_terms = input_query.split()
  query_terms = process(query_terms, stop_words)
process_query(q_id, query_terms, algo, f_name)
