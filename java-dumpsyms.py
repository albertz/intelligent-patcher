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

PrintIdentifiers = True

lastNamespace = []

def handler(p):
	global lastNamespace
	if len(lastNamespace) < len(p.namespace):
		if PrintIdentifiers and not None in p.namespace and set(p.openingTypes) == set("{"): print ".".join(p.namespace)
	lastNamespace = list(p.namespace)

parser = JavaParser()
parser.readStream(infile, handler)

