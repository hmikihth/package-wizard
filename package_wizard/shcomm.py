#!/bin/env python
import sys
import commands

l = len(sys.argv) - 1
i = 1
comm = ''
while i < l:
  comm += sys.argv[i]
  comm += ' '
  i += 1
commands.getoutput(comm)
commands.getoutput('touch '+ sys.argv[l])
