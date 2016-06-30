from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from Models import Base,Document,InvertedIndex
from query import Query
from QueryInfo import QueryInfo
from sets import Set

class DB_Session():
  def __init__(self):
    self.__engine = create_engine('sqlite:///search_engine.db')
    Base.metadata.bind = self.__engine
    DBSession = sessionmaker(bind=self.__engine)
    self.__session = DBSession()

  """
  Add a new document into the table
  """
  def addDocument(self, docID, title, docLen, termsCountStr):
    d = Document(docID=docID, title=title, docLen=docLen, termsCountStr=termsCountStr)
    self.__session.add(d)

  """
  Add a new inverted index entry
  """
  def addIIEntry(self, term, cntTerms, dfTerm, docsCnt):
    e = InvertedIndex(term=term, cntTerms=cntTerms, dfTerm=dfTerm, docsCnt=docsCnt)
    self.__session.add(e)

  """
  Commit changes to the database
  """
  def commit(self):
    self.__session.commit()

  """
  Query a list of Documents from a string
  """
  def getDocsFromQuery(self, query, totalDocs):
    termsCount = query.getTermsCount()
    dfTerms = {}
    docIDs = Set([])
    docs = []
    for term in termsCount.keys():
      query_ret = self.__session.query(InvertedIndex).filter(InvertedIndex.term==term)
      # if no matching document is found
      if query_ret is None or query_ret.count() == 0:
        dfTerms[term] = 0
        continue
      dfTerm = query_ret.first().dfTerm
      dfTerms[term] = dfTerm
      docsCntStr = query_ret.first().docsCnt
      docsCntList = docsCntStr.split(",")
      for i in range(int(dfTerm)):
        docID = docsCntList[2*i]
        if docID in docIDs: continue
        docIDs.add(docID)
        cnt = docsCntList[2*i+1]
        query_ret = self.__session.query(Document).filter(Document.docID==docID)
        doc = query_ret.first()
        docs.append(doc)
    return QueryInfo(query, docs, totalDocs, dfTerms)
