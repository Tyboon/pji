from dataTreatment import *
from fileGestion import *
from learningMethods2 import *

from sys import argv
import getopt

#import weka.core.jvm as jvm

def usage() :
	
	print ""
	print "	learn c cl mc : "
	print "applied learning method on a base containing just cluster digits, another containine cluster and link associated digits and the last containing monomer and cluster digits"
	
	print ""
	print "	compare : "
	print "compare all analyses stocked since the beginning, return a sorted list from the better to the worst digit"
	
	print ""
	print "	show  : "
	print "show the result of the learning method on the cl digits"
	print ""
	
	print "	exit : "
	print "quit the program "
	print ""
	

def start(argv) :
	peptidesFile = 'NORINE'
	monomersFile = 'NORINE'
	clustersFile = 'NORINE'
	selectActivity = -1 
	default = False
	try :
		opts, args = getopt.getopt(argv,"hp:m:c:s:d",["pep=","mono=","clust=","ceil="])
	except getopt.GetOptError :
		print 'main [-p <peptideFile> -m <monomerFile> -c <clusterFile> -d -s <ceil_activite>]'
		print 'by default data from Norine are used, -d = one activity without surfactant'
		sys.exit(2)
	for opt, arg in opts :
		if opt == '-h' :
			print 'main -p <peptideFile> -m <monomerFile> -c <clusterFile>'
			sys.exit()
		elif opt in ("-p", "--pep") :
			peptidesFile = arg
		elif opt in ("-m", "--mono") :
			monomersFile = arg
		elif opt in ("-c", "--clust") :
			clustersFile = arg
		elif opt == '-d' :
		   default = True
		elif opt in ("-s","--ceil") :
			selectActivity = int(float(arg))
		else :
			print 'main -p <peptideFile> -m <monomerFile> -c <clusterFile>'
			sys.exit()
	return peptidesFile, monomersFile, clustersFile, default, selectActivity

if  __name__ == "__main__" :

	peptides_link = read_csv('../file/peptides_all.csv')	
	Y = np.array([x[0] for x in peptides_link])
	Y = Y[1:] # delete header
	X = peptides_link[1:] # delete header
	X = np.array([x[4:] for x in X], dtype=float)
	Y, d = numerize(Y)
	reportBis(X, Y, d)
	
