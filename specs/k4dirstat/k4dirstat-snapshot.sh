#!/bin/sh

version=2.7.4
gitversion=33ed79e

git clone  https://bitbucket.org/jeromerobert/k4dirstat.git  ./k4dirstat
git  --git-dir=./k4dirstat/.git archive --format=tar --prefix=k4dirstat-${version}/ ${gitversion} | bzip2 --best -cf - > k4dirstat-${version}.tar.bz2
