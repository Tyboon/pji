from getDataList import *
from weka_launch import *

from sys import argv
import getopt

def main(argv) :
	peptidesFile = 'NORINE'
	monomersFile = 'NORINE'
	clustersFile = 'NORINE'
	try :
		opts, args = getopt.getopt(argv,"hp:m:c:",["pep=","mono=","clust="])
	except getopt.GetOptError :
		print 'main -p <peptideFile> -m <monomerFile> -c <clusterFile>'
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
		return peptidesFile, monomersFile, clustersFile

if  __name__ == "__main__" :
	##################### ANALYSE ARGUMENTS #######################
	peptidesFile, monomersFile, clustersFile = main(argv[1:])

	print peptidesFile, monomersFile, clustersFile

	##################### LOADING PEPTIDES #########################
	print "Hi, let's start with %s base" % (peptidesFile)

	list_init = load_peptides(peptidesFile)  # charge soit norine soit le csv bdd
	
	print "peptides loaded"

	#################### LOADING MONOMERS #########################
	print "Now, loading monomers from %s" % (monomersFile)

	list_monomers = load_monomers(monomersFile) # charge soit les monomeres de norine soit du csv si precise

	print "monomers loaded"

	#################### LOADING CLUSTERS ##########################
	print "Now loading clusters from %s" % (clustersFile)

	list_clusters = load_clusters(clustersFile)

	print "clusters loaded"

	################################################################
		GENERATE FULL LIST PEPTIDES (MONO, LINK, CLUST)
	################################################################

	




