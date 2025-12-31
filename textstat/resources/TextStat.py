#!/usr/bin/env python3.2
# -*- coding: UTF-8 -*-
# encoding: utf-8


"""
TextStat.py
(C) 2009-2011 by Damir Cavar <http://damir.cavar.me/>

TextStat.py is a module that provides various statistical functions for text
analysis and processing, N-gram model generation, vector space model generation
and processing, and so on.

It is based on Python 3.x.


License

This file is part of the TextStat.py Python 3.x module.

    TextStat.py is free software: you can redistribute it and/or modify
    it under the terms of the GNU Lesser General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    textstat is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Lesser General Public License for more details.

    You should have received a copy of the GNU Lesser General Public License
    along with TextStat.py.  If not, see <http://www.gnu.org/licenses/>.

"""

__author__ =  'Damir Cavar <damir@cavar.me>'
__version__=  '1.0'


import sys, codecs
from collections import Counter
from math import log, sqrt
from operator import itemgetter, mul
from functools import reduce


# make stdout take UTF-8
sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())


df1chi2sigscore = 7.879
"""df1chi2sigscore = 7.879 is the Significance score for the Chi2-test for a degree of freedom of 1."""

CI2EXPECTATIONCOUNTOFF = 0.000000001
NAIVEBAYESIANCOUNTOFF = 0.000000001
RECOUNTOFF = 0.000001


def freqProfile(tokenlist, model=None):
   """Generates a frequency profile from a token list.
      
      Parameter:
      
      tokenlist: an iterable sequence of tokens.
      
      Optional parameter:
      
      model: a dictionary data structure, i.e. a frequency profile
      default = None
      """
   if model:
      return mergeFreqProfiles(model, dict(Counter(tokenlist)))
   else:
      return dict(Counter(tokenlist))


def textKWIC(text, token, contextchars=15, wordboundary=True):
   """Returns a list of left and right context tuples for token.
      The context is default of length 15,
      the context obeys word boundaries in the default.
      !!! TODO !!!
   """
   pos = text.find(token)
   res = []
   while pos > -1:
      left = text[max(0,pos-contextchars):pos].strip()
      right = text[pos+len(token):max(contextchars,len(text)+pos+len(token))].strip()
      res.append( (left, right) )
      if pos + 1 < len(text) + len(token):
         pos = text.find(token, pos + 1)
      else:
         break
   return tuple(res)


def mergeFreqProfiles(freqp1, freqp2):
   """Returns a frequency profile from two merged frequency profiles.
      The two frequency profiles must be dictionary types.
      
      Parameters:
      
      freqp1: dictionary, i.e. frequency profile
      
      freqp2: dictionary, i.e. frequency profile
      
      This function only works with absolute frequency profiles.
      """

   return dict(((i, freqp1.get(i, 0) + freqp2.get(i, 0)) for i in set.union(set(freqp1), set(freqp2))))


def relFreqProfile(freqprof):
   """Generates a relative frequency profile from an absolute frequency
      profile."""
   tokenCount = sum(freqprof.values())
   if tokenCount > 0:
      return dict(((i[0], i[1]/tokenCount) for i in freqprof.items()))


def filterTokens(model, tokenset):
   """Eliminates tokens from tokenset from a model."""
   return dict((i for i in model.items() if i[0] not in tokenset))


def vectorFromModel(model, vectormodel):
   """Returns a vector from a model (e.g. frequency profile),
      matching the token to position table in vectormodel."""
   return tuple(list((model.get(i, 0) for i in vectormodel)))


def positionVectorFromModel(model):
   """Returns a vector with all tokens in model, used to match a token with
      a position in a vector."""
   return tuple(model.items())


def ngramList(tokenlist, n):
   """Returns a N-gram list from a tokenlist.
      The returned list is just a list of N-grams, not a frequency profile."""
   if len(tokenlist) >= n:
      return tuple((tuple(tokenlist[i:i+n]) for i in range(len(tokenlist) - (n - 1))))
   return ()


def relativeEntropyScore(model1, model2):
   """Returns the relative entropy score for two distributions.
      The lower the RE-score, the better!"""
   return sum((model1[i] * log(model1[i]/model2.get(i, RECOUNTOFF), 2) for i in model1))


def dotProduct(vector1, vector2):
   """Returns the dot product of two vectors."""
   if len(vector1) == len(vector2):
      return sum((vector1[i] * vector2[i] for i in range(len(vector1))))
   return None


def cosineSimilarity(vector1, vector2):
   """Returns the cosine similarity of two vectors."""
   if len(vector1) == len(vector2):
      magnitude = sqrt(sum((i**2 for i in vector1))) * sqrt(sum((i**2 for i in vector2)))
      if magnitude > 0:
         return dotProduct(vector1, vector2) / magnitude
   return None


def euclideanDistance(vector1, vector2):
   """Returns the Euclidean distance of two vectors."""
   if len(vector1) == len(vector2):
      return sqrt(sum((vector1[i] - vector2[i])**2 for i in range(len(vector1))))
   return None


def termInDocsProfile(docsprofiles):
   """Returns a profile with terms and number of documents in which the term
      occurs as a key value pair in a dicitionary data structure.
      
      Parameter:
      
      docsprofiles: list with
      a. frequency profiles for documents (dictionary data structure), or
      b. lists or tuples with document tokens
      c. set of document tokens
      """
   mycount = Counter()
   for doc in docsprofiles:
      if type(doc) == type(dict):
         mycount.update(doc.items())
      elif type(doc) == type([]) or type(doc) == type(tuple()):
         mycount.update(set(doc))
      elif type(doc) == type(set()):
         mycount.update(doc)
      else:
         return None
   return dict(mycount)


def tfidfProfile(docfprof, numdocs, termsindocprofile):
   """Returns a document profile after applying tf-idf reranking to it.
   
   Parameters:
   
   docfprof: document frequency profile with absolute frequencies
   
   termsindocprofile: a dictionary data structure with term and count of
   documents it occurs in pairs.
   """
   total = sum(docfprof.values())
   if total > 0:
      return dict((tuple(i, tfidfScore(docfprof[i]/total, numdocs, termsindocprofile[i])) for i in docfprof))
   return None


def tfidfScore(tf, numdocs, numtermincorp):
   """Returns the tf-idf-score for a term.
      
      Parameters:
      
      tf: text frequency of the term, i.e. the relative frequency of a term in
      a document, or number of times a term occurs in a document divided by
      the number of terms in the document.
      
      numdoc: the total number of documents in the corpus, i.e. number of
      documents in all classes.
      
      numtermincorp: number of documents in the corpus in which the term
      occurs.
      """
   return tf * log(numdocs / (1 + numtermincorp))


def naiveBayesianScore(model, tokenlist, pdoc):
   """Returns the Naive Bayesian score given a model and a tokenlist.
      The score is the sum of logs of the document probability and
      the individual token probabilities in the tokenlist, taken from model.
      
      Parameters:

      model: dictionary with token - relative frequency pairs

      tokenlist: iterable list or tuple of tokens

      pdoc: float with the probability to get a document of the class that
            corresponds to the model (this is the number of documents used to
            generate the model for the class, divided by the number of all
            documents.
   """
   return log(pdoc) + sum((log(model.get(i, NAIVEBAYESIANCOUNTOFF)) for i in tokenlist))


def chi2Score(observation, expectation):
   """Returns the Chi2-score for an observation and expectation value list."""
   if len(observation) == len(expectation):
      return sum((observation[i] - max(expectation[i], CI2EXPECTATIONCOUNTOFF))**2 / max(expectation[i], CI2EXPECTATIONCOUNTOFF) for i in range(len(observation)))
   return None


def highestNTermsChi2(docfprof, corpfprof, n=10):
   """Returns a list of the first n tokens with the highest Chi2 score.
      """
   doctotal  = sum(docfprof.values())
   corptotal = sum(corpfprof.values())
   res = [ (j[0], chi2Score(j[1:],expectationFromObservationDF1(j[1:]))) for j in ((i, docfprof.get(i, 0), corpfprof.get(i, 0) - docfprof.get(i, 0), doctotal - docfprof.get(i, 0), corptotal - (corpfprof.get(i, 0) - docfprof.get(i, 0))) for i in docfprof) ]
   res.sort(key=itemgetter(1), reverse=True)
   return (i[0] for i in res[:n])


def significantTermsChi2(docfprof, corpfprof):
   """Returns a list of significant terms from a document, given the documents
      frequency profile and the corpus frequency profile.
      
      The significance test is based on Chi2.
      
      Parameters:
      
      docfprof: absolute frequency profile for one document.
      
      corpfprof: absolute freqeuncy profile for the complete corpus.
      
      It is presupposed that all terms in docfprof are also in corpfprof,
      although, this function is robust wrt. this assumption.
      """
   doctotal  = sum(docfprof.values())
   corptotal = sum(corpfprof.values())
   return (k[0] for k in ((j[0], chi2Score(j[1:],expectationFromObservationDF1(j[1:]))) for j in ((i, docfprof.get(i, 0), corpfprof.get(i, 0) - docfprof.get(i, 0), doctotal - docfprof.get(i, 0), corptotal - (corpfprof.get(i, 0) - docfprof.get(i, 0))) for i in docfprof)) if k[1] >= df1chi2sigscore)


def chi2Significant(tuple, unigrams, bigrams):
   """Returns true, if token1 and token2 are significantly coocurring,
      false otherwise. The used test is the Chi2-test.
      
      Parameters:
      
      tuple: tuple of tokens

      unigrams: unigrams dictionary data structure

      bigrams: bigrams dictionary data structure
   """
   yes_yes = bigrams.get(tuple, 0)
   yes_not = unigrams.get(tuple[0], 0) - yes_yes
   not_yes = unigrams.get(tuple[1], 0) - bigrams.get(tuple, 0)
   not_not = sum(bigrams.values()) - 1 - yes_not - not_yes + yes_yes
   chi2score = chi2Score((yes_yes, yes_not, not_yes, not_not),
      expectationFromObservationDF1((yes_yes, yes_not, not_yes, not_not)))
   if chi2score and chi2score > df1chi2sigscore:
      return True
   return False


def expectationFromObservationDF1(observation):
   """Returns the expectation values for observation values, assuming a table
      of two columns and two rows represented in a value list observations.
      That is, the first two values are assumed to be row 1, the second two
      values are assumed to be row 2.
      
      A table like:
       -----------------------------------
      |           | class     | not class |
      |-----------------------------------|
      | token     | 34        | 4567      |
      | not token | 16356     | 34985737  |
       -----------------------------------

      is mapped on a list like this, i.e. observations is
      ( 34, 4567, 16356, 34985737 )
      
      the returned corresponding expected values would be:
      (2.15417057091995, 4598.84582942908, 16387.84582942908, 34985705.15417057)
      """
   if len(observation) == 4:
      rowtotal1 = sum(observation[:2])
      rowtotal2 = sum(observation[2:])
      columntotal1 = sum(observation[::2])
      columntotal2 = sum(observation[1::2])
      total = sum(observation)
      return ( (rowtotal1 * columntotal1) / total,
               (rowtotal1 * columntotal2) / total,
               (rowtotal2 * columntotal1) / total,
               (rowtotal2 * columntotal2) / total )
   return None



def pointwiseMI(ngram, ngrammodel, unigrammodel):
   """Return the Mutual Information score for an N-gram based on the N-gram
      frquency profile and the individual frequencies.
   """
   return ngrammodel.get(ngram, 0.000000001) * log(ngrammodel.get(ngram, 0.000000001) / reduce(mul, (unigrammodel.get(i, 0.000000001) for i in ngram )), 2)


def MI(ngrammodel, unigrammodel):
   """Returns the sum of the Mutual Information score over the ngrams.
   """
   return sum([ pointwiseMI(ngram, ngrammodel, unigrammodel) for ngram in ngrammodel ])


