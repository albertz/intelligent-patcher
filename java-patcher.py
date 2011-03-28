#!/usr/bin/python

# by Albert Zeyer, www.az2000.de
# code under GPLv3+

import sys
import codecs # utf8
from javaparser import JavaParser

infile = sys.stdin
infilename = len(sys.argv) > 1 and sys.argv[1] or "-"
if infilename == "-": infile = sys.stdin
else: infile = codecs.open(infilename, "r", "utf-8")

lastNamespace = []

def handler(p):
	if p.lastChar != None: sys.stdout.write(p.lastChar.encode("utf-8"))
	global lastNamespace
	if len(lastNamespace) < len(p.namespace):
		if not None in p.namespace and set(p.openingTypes) == set("{"):
			namespaceStr = ".".join(p.namespace)
			if namespaceStr == "Applet":
				sys.stdout.write("\n\n" + p.curScopeIndent + "FOOOO")
	lastNamespace = list(p.namespace)

parser = JavaParser()
parser.readStream(infile, handler)

