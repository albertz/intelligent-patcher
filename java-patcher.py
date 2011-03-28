#!/usr/bin/python

# by Albert Zeyer, www.az2000.de
# code under GPLv3+

import sys
import codecs # utf8
from javaparser import JavaParser
from StringIO import StringIO

infile = sys.stdin
callbacks_newNamespace = {}
infilename = None
inplace = False

i = 1
while i < len(sys.argv):
	arg = sys.argv[i]
	if len(arg) > 1 and arg[0] == "-": # an option
		if arg == "-insertin":
			i += 1
			namespace = sys.argv[i]
			i += 1
			replacefile = sys.argv[i]
			if namespace not in callbacks_newNamespace: callbacks_newNamespace[namespace] = []
			def func(p):
				sys.stdout.write("\n")
				for l in open(replacefile):
					sys.stdout.write("\n" + p.curScopeIndent + l.strip("\n"))
			callbacks_newNamespace[namespace].append(func)
		elif arg == "-inplace":
			sys.stdout = StringIO()
			inplace = True
		else:
			raise Exception, "arg option " + arg + " unknown"
	else:
		infilename = arg
	i += 1

if infilename != "-" and infilename != None: infile = codecs.open(infilename, "r", "utf-8")

lastNamespace = []

def handler(p):
	if p.lastChar != None: sys.stdout.write(p.lastChar.encode("utf-8"))
	global lastNamespace
	if len(lastNamespace) < len(p.namespace):
		if not None in p.namespace and set(p.openingTypes) == set("{"):
			namespaceStr = ".".join(p.namespace)
			if namespaceStr in callbacks_newNamespace:
				for func in callbacks_newNamespace[namespaceStr]: func(p)
	lastNamespace = list(p.namespace)

parser = JavaParser()
parser.readStream(infile, handler)

if inplace:
	infile.close()
	infile = open(infilename, "w")
	infile.write(sys.stdout.getvalue())
	infile.close()
