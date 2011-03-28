#!/usr/bin/python

import sys
import codecs # utf8

infile = sys.stdin
infilename = len(sys.argv) > 1 and sys.argv[1] or "-"
if infilename == "-": infile = sys.stdin
else: infile = codecs.open(infilename, "r", "utf-8")

PrintIdentifiers = True
TABWIDTH = 4

class JavaParser:
	TagWords = ["public","private","protected","final","static"]

	def __init__(self):
		self.namespace = []
		self.openingTypes = []
		self.ignoreNext = False
		self.curWords = []
		self.curWord = ""
		self.curLine = 1
		self.curColumn = 1
		self.inSimpleComment = False
		self.inMultilineComment = False
		self.lastChar = None
	
	def at(self): return "%d:%d" % (self.curLine, self.curColumn)
	def read(self, char):
		lastChar = self.lastChar
		self.lastChar = char
		
		if char == "\n":
			self.curLine += 1
			self.curColumn = 1
			self.inSimpleComment = False
		elif char == "\t":
			self.curColumn += TABWIDTH
		else:
			self.curColumn += 1

		if self.ignoreNext:
			self.ignoreNext = False
			return

		if self.inMultilineComment and lastChar == "*" and char == "/":
			self.inMultilineComment = False
			return
		if self.inMultilineComment or self.inSimpleComment: return

		inQuotes = len(self.openingTypes) > 0 and self.openingTypes[-1] == "\""
		
		if not inQuotes:
			if char.lower() in "abcdefghijklmnopqrstuvwxyz0123456789":
				self.curWord += char
			else:
				if not self.curWord in JavaParser.TagWords and self.curWord != "":
					self.curWords.append(self.curWord)
				self.curWord = ""
			if lastChar == "/" and char == "/":
				self.inSimpleComment = True
				return
			elif lastChar == "/" and char == "*":
				self.inMultilineComment = True
				return

		if char == "\"":
			if inQuotes: self.openingTypes.pop()
			else: self.openingTypes.append("\"")
			return
		if inQuotes:
			if char == "\\": self.ignoreNext = True
			return		
		
		if char in "([{":
			self.openingTypes.append(char)
			self.namespace.append(len(self.curWords) > 0 and self.curWords[0:2][-1] or None)
			self.curWords = []
			if PrintIdentifiers and char == "{" and not None in self.namespace: print ".".join(self.namespace)
		elif char in "}])":
			inBrackets = len(self.openingTypes) > 0 and self.openingTypes[-1] == {")":"(","}":"{","]":"["}[char]
			if not inBrackets: print >>sys.stderr, self.at(), ": closing brackets", char, "have no matching opening brackets"
			else:
				self.openingTypes.pop()
				self.curWords = [self.namespace.pop()]
				if char == "}": self.curWords = []
		elif char == ";":
			self.curWords = []

	def readStream(self, stream):
		while True:
			char = stream.read(1)
			if char == "": break
			self.read(char)


parser = JavaParser()
parser.readStream(infile)

