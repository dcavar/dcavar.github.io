---
layout: post
title:  "Compiling Thrax on Linux, Mac OSX, and Windows with Cygwin"
author: Damir Cavar
date:   2016-07-17 14:34:10 -0400
permalink: compiling-thrax-on-linux-mac-osx-and-windows-with-cygwin
categories: software
tags: C++ CL "Finite State" Language NLP Windows	Cygwin OpenFST Thrax
---
[Thrax] is a grammar compiler developed by a team of researchers at Google Research. It depends on [OpenFST].
See for more details on how to configure and compile [OpenFST].

Download and unpack the source of [Thrax] version 1.2.2 or newer.

See what options configure provides:

    ./configure –help

Since I need the static libraries, I added this option:

    –enable-static

I also enabled the command line binaries:

    –enable-bin

and the *readline library* in the rewrite tester:

    –enable-readline

The last option presupposes that you have installed the devel-package for *libreadline* on your Mac OSX, [Fedora],
[Ubuntu], or Windows with [Cygwin].

You have to have the complete [OpenFST] library compiled and installed on your system. [Thrax] depends on some more
extensions that are not compiled with the default configuration of [OpenFST]. Follow the instructions on the blog
post how to compile [OpenFST].

I also set the environment variable for Windows with [Cygwin]. In particular the library path information seems to be
necessary since the make process might stop with the message that it cannot find *libfst* and *libfstfar*:

    export CXXFLAGS=”-O -D_POSIX_SOURCE  -L/usr/local/lib -I/usr/local/include”

My complete configure command in the *thrax-1.2.2* folder:

    ./configure –enable-static –enable-bin –enable-readline

To avoid issues with undefined ACCESSPERMS in the file *thrax-1.2.2/src/lib/util/utils.cc* you can add these three
lines of code below the include statements (for example below line 31):

    #ifndef ACCESSPERMS
    #define ACCESSPERMS (S_IRWXU|S_IRWXG|S_IRWXO)
    #endif

The maintainers of the [Thrax] code-base might want to add this anyway, since some operating systems do not declare
ACCESSPERMS in the default. [Cygwin] on Windows does not.

To compile [Thrax] run:

    make

Then follow up with a:

    make install

On Mac OSX or Linux you might want to prepend a *sudo* to the command above.

That was it.


[Thrax]: http://openfst.cs.nyu.edu/twiki/bin/view/GRM/Thrax "Thrax"
[OpenFST]: http://www.openfst.org/twiki/bin/view/FST/WebHome "OpenFST"
[Fedora]: https://getfedora.org/ "Fedora"
[Ubuntu]: http://www.ubuntu.com/ "Ubuntu"
[Cygwin]: http://cygwin.com/ "Cygwin"
