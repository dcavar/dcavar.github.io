---
title:  CSCI-B 659 and LING-715 Semantic Natural Language Processing, NoAI, and Big Knowledge
layout: post
author: Damir Cavar
date:   2017-06-29 20:14:10 -0400
permalink: Semantic_NLP_NoAI_Big_Knowledge
categories: software, course, AI, spoken language interface, knowledge graph
tags: Graph-DB Alexa "Google Assistant" OWL NLP LFG "Dependency Parser" "Lexical-functional Grammar" textmining "deep parsing" "knowledge graphs"
---

This fall I am teaching the course:

CSCI-B 659 TOPICS ARTIFICIAL INTELLIGENCE (and LING-L 715 SEMINAR IN COMPUTATIONAL LING) (3 CR)

VT: SEMANTICS AND DISCOURSE

10761 PERM     09:30A-10:45A   TR     BH 221    Cavar D                   8    6    0
- Above class open to graduates only
- Above class requires permission of instructor
- Above class meets with LING-L 715 

(Note: *This is not CSCI-B 659/LING-L 645 Topics in Artificial Intelligence/Advanced NLP!*)


## Topic: Semantic Natural Language Processing, NoAI, and Big Knowledge

The goal of this seminar is to understand theoretical and practical aspects of:

- systems (similar to some version of IBM Watson) that read unstructured text and map content on knowledge representations using ontologies, networks, and Graph-databases,
- developing a natural language frontend (what is now referred to as AI by Amazon or Google) using the Alexa SDK and/or Google Assistant to query with spoken language the knowledge representation or have a longer conversation about some concrete topic.

Our goal is to set up a fully functional system by end of the semester.


### Issues

This is a theoretical and also very practical seminar that includes:

- setting up a test server on the Amazon AWS (EC2) cloud (and/or Microsoft Azure) using Linux as an operating system
- using common (and lesser common) NLP technologies and pipelines for text processing, parsing, semantic analysis
- modeling grammars (using deep linguistic models, e.g. Probabilistic Lexical-functional Grammar, Construction Grammar), linguistic processing of morphologies (using Finite State Transducer and various probabilistic models), multi-word expressions, concept typing, etc.
- using Graph Databases for knowledge representations (e.g. Neo4J, Apache Jena, Stardog), using SPARQL, Reasoning engines (e.g. Fact++, Pellet), OWL2, semantic constraints over OWL2
- using the Amazon Alexa SDK and Lambda Functions for the development of spoken language interfaces to query knowledge representations
- various machine learning technologies, neural networks, graph and network analysis technologies that are related to NLP and knowledge representations/processing
- all based on truly open source code and tools from our side (with the exception of Amazon's or Google's SDKs)

Students from Linguistics and language studies will gain experience with the newest technologies that are underlying applications like Amazon Alexa, Google Assistant, IBM Watson, etc. They will have the opportunity to model linguistic knowledge (lexical, syntactic, semantic, pragmatic) and apply it in high-level technological environments.

Students from Data Science, Computer Science, Engineering, will gain experience with real advanced NLP technologies and methods, open source projects, industry relevant APIs and technologies.

Cognitive Science students will gain experience with modeling of concept nets and knowledge representations, real applications with NLP, machine learning, and AI algorithms.

The course will group students into projects with priorities on modeling linguistic processing and analysis, knowledge representations and graph-based technologies, spoken language interfaces using common SDKs and APIs from Amazon and Google, etc., depending on the students core skills and main interests.


### Research Questions

The content of the course can have these special foci, among others:

- Using deep parsing (beyond shallow Dependency Parsing or simple Constituent Structure) of unstructured text to extract semantically relevant concepts and content and map the parsed concepts and relations on networks and graph-based knowledge representations.
- We can discuss the issues with current shallow parsing and NLP methods and how we can generate representations that are closer to a semantic representation (including scope, functional relations, concept classification), that can be mapped onto a Description Logic, potentially a Linear Logic or Glue Semantics.
- Using knowledge representations (graphs and networks) we can apply techniques for validation and verification of content (using Description Logic and general network analysis strategies). This would be related to Fake News or Deception detection in textual content sources.
- Using spoken language query processing (via Alexa or Google Assistant) we can generate spoken language responses using a query to SPARQL to template language generation mapping.
- Using various neural network strategies we can approach modeling of dialog memory, co-reference analysis, or simple processing of different discourse functions.
- Using temporal logic we can process time references and deduce the event time of assertions.
- Using dialog memory and pragmatic components and modeling technologies we can manage not only co-reference and anaphoric relations, but also complex conversation flow and conversational goals.

