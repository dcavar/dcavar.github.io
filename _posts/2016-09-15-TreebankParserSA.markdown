---
layout: post
title:  "TreebankParser SA"
author: Damir Cavar
date:   2016-09-15 15:10:00 -0400
permalink: treebankparser-sa
categories: software
tags: C++ PCFG Treebank "Natural Language Processing" "Machine Learning" ML NLTK FLE LFG WFST, Corpora
---
I posted the code of the standalone version of the
[TreebankParser on Bitbucket](https://bitbucket.org/dcavar/treebankparsersa/).
A [binary for Mac OSX](https://bitbucket.org/dcavar/treebankparsersa/downloads/MacOSX-64-treebankparser.zip)
can be found in the [Download section](https://bitbucket.org/dcavar/treebankparsersa/downloads).
Binaries for the common operating systems will follow.

The [TreebankParser](https://bitbucket.org/dcavar/treebankparsersa/) is part of the
[Free Linguistic Environment](http://gorilla.linguistlist.org/fle/) ([FLE](http://gorilla.linguistlist.org/fle/))
project. It converts some types of treebanks to a set of rules with frequencies or probabilities.
Some extensions that are part of FLE will be added soon, e.g. converting the Context-free Grammars (CFGs)
into a Weighted Finite State Transducer (WFST) representation.
