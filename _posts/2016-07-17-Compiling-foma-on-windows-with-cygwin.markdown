---
layout: post
title:  "Compiling Foma on Windows with Cygwin"
author: Damir Cavar
date:   2016-07-17 18:25:00 -0400
permalink: compiling-foma-on-windows-with-cygwin
categories: software
tags: Foma "Natural Language Processing" "Machine Learning" ML NLTK FLE LFG WFST Corpora
---
[Foma] comes as a package in the standard distribution of [Ubuntu]. However, it might be necessary to recompile it,
if you intend to link the static library to your software, since the static library was missing in the
[16.04 LTE distro](http://www.ubuntu.com/) that I tested. You can uninstall the fedora package and use the same
instructions below to compile your own version with all components (i.e. binaries, dynamic and static libs,
and include files) for [Ubuntu] 16.04 or [Fedora] 24. In fact, the same is true for compilation on the most recent
Mac OSX with Xcode.

I got the [Foma] source from the [GitHub site](https://fomafst.github.io/) using the *foma-0.9.18.tar.gz* file.

In the unpacked folder *foma-0.9.18*. I edited the *Makefile*. In **line 16** I changed the line:

    LDFLAGS = -lreadline -lz -ltermcap

by removing the *-ltermcap* parameter to get:

    LDFLAGS = -lreadline -lz

I saved the changed *Makefile*.

In [Cygwin] I made sure that all the development tools are installed, and in particular the package *libreadline-devel*.

To compile [Foma] I ran:

    make

To install the libraries and include-files I ran:

    make install

You could prepend the command above with *sudo* on Mac OSX or Linux. The components can be found in the subfolders
*bin*, *lib*, *include* of */usr/local*.

That is all.



[Foma]: https://fomafst.github.io/ "Foma"
[Ubuntu]: https://www.ubuntu.com/ "Ubuntu"
[Fedora]: https://getfedora.org/ "Fedora"
