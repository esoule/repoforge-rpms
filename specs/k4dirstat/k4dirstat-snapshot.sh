#!/bin/sh

version=2.7.0
gitversion=6c0a9e6

git clone http://grumpypenguin.org/~josh/kdirstat.git
git archive --format=tar --prefix=k4dirstat-${version}/ --remote=kdirstat ${gitversion} | bzip2 --best -cf - > k4dirstat-${version}.tar.bz2
