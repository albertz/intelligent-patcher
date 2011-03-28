#!/usr/bin/python

import sys
import codecs # utf8

infile = sys.stdin
infilename = sys.argv[1] or "-"
infilename = "/Users/az/Programmierung/EclipseWorkspace/Ilias/Lehreinheiten/Abbildungen/Code/applets/Abbildungen_I03_Abbildungen/Applet.java"
if infilename == "-": infile = sys.stdin
else: infile = codecs.open(infilename, "r", "utf-8")

TABWIDTH = 4
JavaIdentifiers = ["class","public","private","protected","final"]

class JavaParser:
	def __init__(self):
		self.namespace = []
		self.openingTypes = []
		self.ignoreNext = False
		self.lastIdentifier = ""
		self.curWord = ""
		self.curLine = 1
		self.curColumn = 1

	def at(self): return "%d:%d" % (self.curLine, self.curColumn)
	def read(self, char):
		if char == "\n":
			self.curLine += 1
			self.curColumn = 1
		elif char == "\t":
			self.curColumn += TABWIDTH
		else:
			self.curColumn += 1

		if self.ignoreNext:
			self.ignoreNext = False
			return
		
		inQuotes = len(self.openingTypes) > 0 and self.openingTypes[-1] == "\""
		
		if not inQuotes:
			if char.lower() in "abcdefghijklmnopqrstuvwxyz0123456789":
				self.curWord += char
			else:
				if not self.curWord in JavaIdentifiers and self.curWord != "":
					self.lastIdentifier = self.curWord
					print self.at(), ": new identifier:", self.lastIdentifier
				self.curWord = ""
		
		if char == "\"":
			if inQuotes: self.openingTypes.pop()
			else: self.openingTypes.append("\"")
			return
		if inQuotes:
			if char == "\\": self.ignoreNext = True
			return		
		
		if char in "([{":
			self.openingTypes.append(char)
			self.namespace.append(self.lastIdentifier)
		elif char in "}])":
			inBrackets = len(self.openingTypes) > 0 and self.openingTypes[-1] == {")":"(","}":"{","]":"["}[char]
			if not inBrackets: print >>sys.stderr, self.at(), ": closing brackets", char, "have no matching opening brackets"
			else:
				self.openingTypes.pop()
				self.namespace.pop()

	def readStream(self, stream):
		while True:
			char = stream.read(1)
			if char == "": break
			self.read(char)


parser = JavaParser()
parser.readStream(infile)

