---
layout: post
title:  "On Ubuntu/Debian/... tools for linguists"
author: Damir Cavar
date:   2016-08-14 13:48:10 -0400
permalink: on-ubuntudebian-tools-for-linguists
categories: software
tags: Corpora NLP Speech Debian Ubuntu "Natural Language Processing" "Machine Learning" ML NLTK FLE WFST
---
### DRAFT – Work in Progress

The standard [Ubuntu] distribution comes with various linguistic tools. I am linking here to 16.04(.1).

Various Finite State Transducer toolkits can be found in the package list that are used for the development of
morphological analyzers, tokenizers, and other NLP tools:

- [Helsinki Finite-State Transducer Technology] ([hfts])
- [Stuttgart finite-state transducer tools] ([sfst])
- [Foma], [Xerox-compatible finite-state compiler - library] ([foma-bin])
- [Ragel] compiles finite state machines into code ([ragel])

There are also ready NLP tools for various languages in the standard package list:

- [Chasen], a Japanese Morphological Analysis System ([chasen])
- [Juman], Japanese morphological analysis system ([juman])
- [Frog], a morphosyntactic tagger, lemmatizer, morphological analyzer, and dependency parser for Dutch. (seems to be missing in the new distro) (see [frogdata])

 
### Other Repositories

Some repositories provide more packages that might be interesting or useful for linguistic work, be it language
documentation or corpus linguistics:

- [Text Encoding Initiative] ([TEI]) XML Schema and XSLT files
- [SIL repository] for [Ubuntu] with most recent versions of fonts, and the [FieldWorks Language Explorer] ([FLEx]) for [Ubuntu]
- ...

I set up the [SIL repository] by creating as root or using sudo a file:

    /etc/apt/sources.list.d/sil.list

with this content for [Ubuntu] xenial (16.04):

    deb http://packages.sil.org/ubuntu xenial main




[Foma]: http://packages.ubuntu.com/xenial/foma-bin "Foma Ubuntu package"
[Xerox-compatible finite-state compiler - library]: http://packages.ubuntu.com/xenial/foma-bin "Foma Ubuntu package"
[foma-bin]: http://packages.ubuntu.com/xenial/foma-bin "Foma Ubuntu package"
[sfts]: http://packages.ubuntu.com/xenial/sfst "Stuttgart finite-state transducer tools"
[hfts]: http://packages.ubuntu.com/xenial/hfst "Helsinki Finite-State Transducer Technology"
[Helsinki Finite-State Transducer Technology]: http://packages.ubuntu.com/xenial/hfst "Helsinki Finite-State Transducer Technology"
[Stuttgart finite-state transducer tools]: http://packages.ubuntu.com/xenial/sfst "Stuttgart finite-state transducer tools"
[Ragel]: http://packages.ubuntu.com/xenial/ragel "Ragel"
[ragel]: http://packages.ubuntu.com/xenial/ragel "Ragel"
[Chasen]: http://packages.ubuntu.com/xenial/chasen "a Japanese Morphological Analysis System"
[chasen]: http://packages.ubuntu.com/xenial/chasen "a Japanese Morphological Analysis System"
[Juman]: http://packages.ubuntu.com/xenial/juman "Japanese morphological analysis system"
[juman]: http://packages.ubuntu.com/xenial/juman "Japanese morphological analysis system"
[Frog]: http://packages.ubuntu.com/xenial/frogdata "a morphosyntactic tagger, lemmatizer, morphological analyzer, and dependency parser for Dutch"
[frogdata]: http://packages.ubuntu.com/xenial/frogdata "a morphosyntactic tagger, lemmatizer, morphological analyzer, and dependency parser for Dutch"
[Text Encoding Initiative]: http://wiki.tei-c.org/index.php/TEIDebian "TEI XML Debian repo"
[TEI]: http://wiki.tei-c.org/index.php/TEIDebian "TEI XML Debian repo"
[FieldWorks Language Explorer]: http://fieldworks.sil.org/flex/ "FieldWorks Language Explorer"
[FLEx]: http://fieldworks.sil.org/flex/ "FieldWorks Language Explorer"
[SIL repository]: http://packages.sil.org/ "SIL repository for Ubuntu"
[Ubuntu]: https://www.ubuntu.com/ "Ubuntu distribution"
