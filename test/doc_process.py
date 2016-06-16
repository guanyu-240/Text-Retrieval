"""
-------------------------------------------------------------------------------
About: Build inverted index
Author: Guanyu Wang
Date: 6-16-2016
-------------------------------------------------------------------------------
"""
from stemming.porter2 import stem

def char_valid(c):
  if c >= '0' and c <= '9':
    return True
  elif c >= 'A' and c <= 'Z':
    return True
  elif c >= 'a' and c <= 'z':
    return True
  else: return False

def process_word(w, stop_words):
  if w is None or w == '': return None
  n = len(w)
  start_idx = 0
  end_idx = n
  while start_idx < n and char_valid(w[start_idx]) == False:
    start_idx += 1
  while end_idx > start_idx and char_valid(w[end_idx-1]) == False:
    end_idx -= 1
  if start_idx == end_idx: return None
  w = w[start_idx : end_idx].lower()
  if w in stop_words: return None
  return stem(w)

def process(words, stop_words):
  ret = filter(lambda x: x != None, 
               map(lambda x: process_word(x, stop_words), words))
  return ret
