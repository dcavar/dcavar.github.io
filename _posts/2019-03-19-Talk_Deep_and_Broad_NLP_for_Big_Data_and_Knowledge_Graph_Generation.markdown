---
title:  Deep and Broad NLP for Big Data and Knowledge Graph Generation
layout: post
author: Damir Cavar
date:   2019-03-19 09:10:00 -0400
permalink: 2019-03-19-Talk_Deep_and_Broad_NLP_for_Big_Data_and_Knowledge_Graph_Generation
categories: Research
tags: NLP Knowledge-Graph Natural-Language-Processing JSON-NLP Big-Data RESTful Microservice
---
## RESTful Microservice API for NLP, JSON-NLP, and Knowledge Graphs

**Talk at Indiana University, School of Informatics, Computing and Engineering (SICE), Luddy Hall, room 1106**

**03/22/2019   10:00 AM**


We present our a new research, development, and integration results
related to:
- broad and deep NLP components in a scalable big data targeting
architecture and API,
- a new NLP annotation standard and Middleware [JSON-NLP](https://github.com/dcavar/JSON-NLP), and
- HooSIER (HooSIER Semantic Information ExtractoR) our approach to
extract core semantic information and Knowledge Graphs (KG) from
unstructured text.

We are using a hybrid ensemble of NLP technologies consisting of
knowledge based, probabilistic and neural NLP and Information
Extraction methods. The underlying technology represents a new kind of
NLP API and system architecture that addresses common limitations of
open and free NLP technologies by providing a scalable and robust
environment. The parallel RESTful Microservice architecture of the NLP
API addresses the lack of standardized and uniform output annotations
by providing our new [JSON Schema for NLP](https://github.com/dcavar/JSON-NLP) that together with the API
abstraction layer also represents a new form of an NLP Middleware.
Numerous common and popular NLP pipelines and environments are
integrated in this new infrastructure, optimizing their performance and
runtime, simplifying the access and management, and making the outputs
accessible for advanced NLP-based engineering.

We also present a novel Information Extraction system and text to KG
generator (HooSIER), which is domain independent and easily adaptable
towards domain specific texts and Information Extraction. It is based
on our unified ensemble of Natural Language Processing (NLP)
Microservice pipelines. It utilizes lexical, syntactic, semantic, and
pragmatic analyses based on their output, including entity and Part-of-
Speech (POS) tagging, lexical analysis, syntactic constituency and
dependency parsers, anaphora and coreference analysis, and unique
approaches to presupposition and implicature computation. Our approach
is capable of predicting implied entities and arguments, from implicit
subjects, over discourse linked implied arguments, to certain
predicates in gapping constructions, and arguments that were subject to
ellipsis. The extraction of core semantic relations based on predicate
argument structures at the clause level yields abstract graph
representation between entities and concepts in the text that represent
core semantic content. Entities and relations are typed and linked
against existing large KGs using common word and graph embedding
disambiguation approaches. Our platform is also capable of generating
probabilistic KGs with typed and linked entities.

The core NLP API will soon be available to the general community on the
IUB campus. The project is a result of year long research and
development activities that included students and colleagues from the
different schools at IU Bloomington, and also external collaborators.
We should emphasize that significant contribution came from the
volunteers and NLP enthusiasts from the [NLP Lab](http://nlp-lab.org/).
