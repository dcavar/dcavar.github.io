---
layout: post
title:  "Compiling OpenFST on Windows 10 using Cygwin"
author: Damir Cavar
date:   2016-07-17 19:42:00 -0400
permalink: compiling-openfst-on-windows-10-using-cygwin
categories: software
tags: OpenFST "Natural Language Processing" "Machine Learning" ML NLTK WFST C++ "Finite State" Cygwin Windows
---
What might compile on [Fedora] or [Ubuntu] out of the box, can be somewhat more complicated on Windows. Assuming
that you are able to set up [Cygwin] on your [Windows 10] (in my case) and also install all the development tools
(e.g. GCC, G++, bison, flex, etc.), here is how I compiled the newest [OpenFST] (v. 1.5.3 in this case) library and
tools for [Cygwin] (doing a compilation to DLLs for Windows native based on Visual Studio 2015 or so might follow soon):

To avoid issues with the *file too big* error during compilation, switch on optimization in C++
(capital O like in Omega):

    -O

To avoid issues with errors like *‘fileno’ was not declared in this scope* one needs to compile the code with
POSIX_SOURCE set.

In the [Cygwin] bash set the environment variables (first one is not necessary):

    export CFLAGS=-D_POSIX_SOURCE
    export CXXFLAGS=”-O -D_POSIX_SOURCE”

In the source folder *openfst-1.5.3* run configure. Check for the modules and extensions that you want to have compiled
(use for example *./configure –help*) I activated most of the extensions for use in or required by other tools and libraries:

    ./configure –enable-static –enable-bin –enable-compact-fsts –enable-compress –enable-const-fsts –enable-far –enable-linear-fsts –enable-lookahead-fsts –enable-mpdt –enable-ngram-fsts –enable-pdt


If you want the Python extensions, add this parameter and make sure that your Python-dev package is installed:

    –enable-python

Compile the code using:

    make

Install it in the [Cygwin] file-structure:

    make Install

That is it.



[OpenFST]: http://www.openfst.org/twiki/bin/view/FST/WebHome "OpenFST"
[Fedora]: https://getfedora.org/ "Fedora"
[Ubuntu]: http://www.ubuntu.com/ "Ubuntu"
[Cygwin]: http://cygwin.com/ "Cygwin"
[Windows 10]: https://www.microsoft.com/en-us/windows/default.aspx "Windows 10"
