from sqlalchemy import Column, Integer, String, Float 
from sqlalchemy.orm import relationship, backref,reconstructor
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

Base = declarative_base()

class Document(Base):
  __tablename__ = 'document'
  docID = Column(String(10), primary_key = True)
  title = Column(String(25), nullable = False)
  docLen = Column(Float, nullable = False)
  termsCountStr = Column(String)

  @reconstructor
  def init_on_load(self):
    self.termsCount = {}
    tmp_list = self.termsCountStr.split(" ")
    for i in range(len(tmp_list)/2):
      term = tmp_list[2*i]
      cnt = int(tmp_list[2*i+1])
      self.termsCount[term] = cnt

  def getTermsCount(self):
    return self.termsCount

  def getDocLen(self):
    return self.docLen
  
class InvertedIndex(Base):
  __tablename__ = 'inverted_index'
  term = Column(String, primary_key = True)
  cntTerms = Column(Float, nullable = False)
  dfTerm = Column(Float, nullable = False)
  docsCnt = Column(String)
  

engine = create_engine('sqlite:///search_engine.db')
Base.metadata.create_all(engine)
