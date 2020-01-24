---
layout: post
title:  "Repairing ELAN annotation files from before 2005 for use with ELAN 4.9.4 or newer"
author: Damir Cavar
date:   2016-08-08 16:43:32 -0400
permalink: repairing-elan-annotation-files-from-before-2005-for-use-with-elan-4-9-4-or-newer
categories: software
tags: Corpora Documentation Language ELAN Python Bash EAF
---
[ELAN] 4.9.4 has issues with older versions of [ELAN] Annotation Files (EAFs).

We noticed that [ELAN] annotation files (EAFs) from 2004 and earlier would not open in [ELAN] 4.9.4, the most recent
version of it. The problem is somewhat serious in that it does not alert one or show the reason for not showing any
tiers or annotations. [ELAN] 4.9.4 would open the files without any specific notification and just showing an empty
tiers and media section.

Han Sloetjes informed me that [ELAN] has a log dialog under *View > View Log…*. We identified the issue to be a
missing attribute in the older EAF XML. The old XML root tag looks like this:

    <ANNOTATION_DOCUMENT AUTHOR="Jarrod Slocum"
    DATE="2004.03.02 13:56 CST"
    FORMAT="2.0" VERSION="2.0"
    xsi:noNamespaceSchemaLocation="http://www.mpi.nl/tools/elan/EAFv2.0.xsd">

This root tag is missing one important attribute that the newer [ELAN] XML-parser requires. Han sent me this change
suggestion:

    <ANNOTATION_DOCUMENT AUTHOR="Jarrod Slocum" DATE="2004.03.02 13:56 CST"
     FORMAT="2.0" VERSION="2.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
     xsi:noNamespaceSchemaLocation="http://www.mpi.nl/tools/elan/EAFv2.0.xsd">

This adds the attribute:

    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"

The issue with this problem is that many linguists working on [ELAN] annotations and opening older EAFs will
potentially get confused and might assume that they lost the data and start writing over the old EAFs and really
lose the previous data and work. Please be aware of this issue and if you have archived EAFs from 2005 or earlier,
you might have to correct the EAF XML to be able to view and edit it in the most recent [ELAN].

I told Han that it might be a good idea to include the code in new [ELAN] releases to correct this error
automatically, since many archived files might be affected by this issue.

If you have a lot of older [ELAN] files with this issue, here is a script or set of commands that will add this
attribute to the XML. You will need some version of Python 3.x to run this script. If you run this in an Unix
environment (Mac OS X, Linux, Windows 10 with Linux Subsystem and Bash), you will also need *find*. This script
will create a backup-copy of all EAFs that are repaired. I strongly recommend that you create your own backup copy
and verify that the repaired EAFs can be opened with the newer versions of [ELAN].

To repair all EAFs in the local folder, assuming that the script [elanrepair.py](/Software/elanrepair.zip) is executable:

    ./elanrepair.py *.eaf

Download the script [elanrepair.py](/Software/elanrepair.zip) in the ZIP-file [elanrepair.zip](/Software/elanrepair.zip).

If the you cannot run the script directly, use the Python 3 interpreter to run it:

    python3  ./elanrepair.py *.eaf

If you want to recurse through a larger set of sub-folders in a bash-command line try:

    find . -name "*.eaf" -type f -exec ./elanrepair.py {} \;

Let me know, if there are any issues with that.

Damir


[ELAN]: https://tla.mpi.nl/tools/tla-tools/elan/ "ELAN"

