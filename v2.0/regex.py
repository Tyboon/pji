#!/usr/bin/env python
import re, sys, os

'''
NRP = Monomer(,Monomer)*(@[0-9](,[0-9])*)+

Unit = (Maj|Min)(-[(Maj)(Min)])*

Maj = [0-9]?[A-Z]+[a-z]*[0-9]*[a-z]*[0-9]*point*parenthese?

Min = [0-9]?[a-z]+[A-Z]*[a-z]*[0-9]*[a-z]*[0-9]*point*parenthese?

point = (:[0,9]+)

parenthese = \([a-z]*[0-9]+(.[a-z]*[0-9]+)*\)

monomer = (([0-9]?[A-Z]+[a-z]*[0-9]*[a-z]*[0-9]*(:[0-9]+)*(\([A-Z]*[a-z]*[0-9]+(.[A-Z]*[a-z]*[0-9]+)*\))?)|([0-9]?[a-z]+[A-Z]*[a-z]*[0-9]*[a-z]*[0-9]*(:[0-9]+)*(\([A-Z]*[a-z]*[0-9]+(.[A-Z]*[a-z]*[0-9]+)*\))?))(-(([0-9]?[A-Z]+[a-z]*[0-9]*[a-z]*[0-9]*(:[0-9]+)*(\([A-Z]*[a-z]*[0-9]+(.[A-Z]*[a-z]*[0-9]+)*\))?)|([0-9]?[a-z]+[A-Z]*[a-z]*[0-9]*[a-z]*[0-9]*(:[0-9]+)*(\([A-Z]*[a-z]*[0-9]+(.[A-Z]*[a-z]*[0-9]+)*\))?)))*

#################################################################################################################################################################"

Unit = \w+(:[0-9]+)*(\(\w+(\.\w+)*\))?


Monomer = Unit(-Unit)*
\w+(:[0-9]+)*(\(\w+(\.\w+)*\))?(-\w+(:[0-9]+)*(\(\w+(\.\w+)*\))?)*

NRP = Monomer(,Monomer)*(@[0-9]+(,[0-9]+)*)+
\w+(:[0-9]+)*(\(\w+(\.\w+)*\))?(-\w+(:[0-9]+)*(\(\w+(\.\w+)*\))?)*(,\w+(:[0-9]+)*(\(\w+(\.\w+)*\))?(-\w+(:[0-9]+)*(\(\w+(\.\w+)*\))?)*)*(@[0-9]+(,[0-9]+)*)+
'''
NRP = '\w+(:[0-9]+)*(\(\w+(\.\w+)*\))?(-\w+(:[0-9]+)*(\(\w+(\.\w+)*\))?)*(,\w+(:[0-9]+)*(\(\w+(\.\w+)*\))?(-\w+(:[0-9]+)*(\(\w+(\.\w+)*\))?)*)*(@[0-9]+(,[0-9]+)*)+'


def regex(file, pattern = NRP) :
	for line in open(file).readlines():
		if re.match(pattern, line):
            		print line

def match(data, pattern = NRP) :
	pat = re.compile(pattern)
	m = pat.match(data)
	if m == None: 
		return False 
	if m.group() == data :
		return True
	return False


if __name__ == ("__main__") :
	print match(sys.argv[1])
