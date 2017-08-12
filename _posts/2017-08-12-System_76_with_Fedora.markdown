---
title:  System 76 Lemur with Fedora 26 KDE Spin
layout: post
author: Damir Cavar
date:   2017-08-12 08:21:00 -0400
permalink: System_76_with_Fedora
categories: System76, Lemur, laptop, Fedora, KDE, Linux
tags: System76 Fedora KDE
---

I installed successfully [Fedora 26 KDE Spin with Plasma Desktop](https://spins.fedoraproject.org/kde/) on my [System 76 Lemur](https://system76.com/laptops/lemur). The default [Ubuntu](https://www.ubuntu.com/) had issues with many things, most annoying were issues with the wireless driver.

As for the procedure:

- Backup your [System 76](https://system76.com/) data and other details (e.g. installed packages, */usr/local*, */opt*, some settings from */etc*).
- Download [Fedora](https://getfedora.org/), in my case the [Fedora 26 KDE Plasma Desktop](https://spins.fedoraproject.org/kde/download/index.html).
- Create a bootable USB Flash drive using [Etcher](https://etcher.io/).
- Plug it into the USB port.
- Boot the [System 76](https://system76.com/) holding down F7 to get into the boot menu.
- Select the USB drive with [Fedora](https://getfedora.org/) to boot from.
- Follow the installation instructions.
- Update the system after successful installation (using *[dnf](https://en.wikipedia.org/wiki/DNF_(Fedora)) update* in the terminal as sudo) and set up some essential software.
- I added the [RPM Fusion repos](https://rpmfusion.org/) and *Yumex-[DNF](https://en.wikipedia.org/wiki/DNF_(Fedora))* via [COPR](https://copr.fedorainfracloud.org/coprs/timlau/yumex-dnf/).
- Play back some backup data and my home directory from the previous installation.
- Et voilà: more up to date operating system, newer kernel, newer compilers, etc.

The only thing that I do not like is the default partitioning schema in the [Fedora](https://getfedora.org/) installation. It creates a partition for the system (mounted at "/"), and one for the user home (mounted at "/home"). When setting up the partition schema, I let [Fedora](https://getfedora.org/) set the default and then remove the "/home" partition and extend the root partition to maximum, that is the entire space. The partitioning tool shows you in the left corner at the bottom the entire space on your drive. I also chose to encrypt the drive, by the way.


Interesting questions:

- Will all devices work?
- Will the wirless work?
- What about an encrypted drive on a SSD? Is it configured correctly so that the TRIM function works?
- What about suspend and wake up?
- Does my [Overleaf](https://www.overleaf.com/), [Office365](https://www.office.com/), [iCloud](https://www.icloud.com/), [Dropbox](https://www.dropbox.com/install-linux), [Netflix](https://www.netflix.com/), ... work?


## Summary

If I encounter issues with something, I will report here.

So far I did not encounter any issues with devices and drivers.

- The [KDE Plasma Desktop](https://www.kde.org/plasma-desktop) works just fine. (Finally no more [Unity](https://unity.ubuntu.com/), no more depressing [GNOME](https://www.gnome.org/)... :-) ).
- The default settings seem to be allowing my encrypted drive to apply the TRIM function.
- Suspend in the default configuration did work even with the lid-close. Surprising was, it did work with the lid-open. [Fedora](https://getfedora.org/) wakes up when you open the lid!
- Some commercial software comes only with a *Debian* package. Use *alien* to set those up. Most important packages (say [Oracle JDK](http://www.oracle.com/technetwork/java/javase/downloads/index.html)) are available as [RPM](https://en.wikipedia.org/wiki/Rpm_(software))-packages. My favorite [JetBrains](https://www.jetbrains.com/) IDEs like [CLion](https://www.jetbrains.com/clion/), [PyCharm](https://www.jetbrains.com/pycharm/), [WebStorm](https://www.jetbrains.com/webstorm/), [IntelliJ IDEA](https://www.jetbrains.com/idea/) work just fine. I set those up in */opt*, create a generic symbolic link to the original folder, configure a PATH variable in */etc/profile.d*, repair the *.desktop*-files to point to the generic symbolic link folder to catch future updates.
- Other software packages come with an [RPM](https://en.wikipedia.org/wiki/Rpm_(software)), as for example [Google Chrome](https://www.google.com/chrome/browser/desktop/index.html), [Brave](https://github.com/brave/browser-laptop/blob/master/docs/linuxInstall.md), or [Dropbox](https://www.dropbox.com/install-linux).
- I am using [LaTeX](https://www.tug.org/texlive/), [LyX](https://www.lyx.org/), or online services like [Overleaf](https://www.overleaf.com/) and [Office365](https://www.office.com/), but even Apple's [iCloud](https://www.icloud.com/) works just fine in a browser.
- You can watch [Netflix](https://www.netflix.com/) in [Firefox](https://www.mozilla.org/en-US/firefox/) now. You will need to accept the extra [DRM](https://en.wikipedia.org/wiki/Digital_rights_management) package the first time when you start watching some movie, but it works just fine.

