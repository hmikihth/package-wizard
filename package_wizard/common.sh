#!/bin/sh

rm -f core.* gui/*.bak rpmanager.pyc
msgfmt ./messages.po -o locale/hu/LC_MESSAGES/rpmanager.mo
cd ..
tar -c $exclusions rpmanager | bzip2 -9 > $target
