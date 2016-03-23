#!/usr/bin/env python3
#Author: Arpan Man Sainju
#Date: 02/17/2016
#Description: contains main functions that calls scanner module of cscanner class. 
import sys
import parser
import helper
def main():
	if len(sys.argv) == 2:
		source = sys.argv[1]
		oparser = parser.cparser(source)
		parsetree = oparser.parser()
	else:
		print("Please provide the file name.\nSyntax : $scanner filename")

main()