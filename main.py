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
	bound_init = len(list_init[0])

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
	######  GENERATE FULL LIST PEPTIDES (MONO, LINK, CLUST)	#######
	################################################################
	
	print "create monomers count"
	peptides_mono = add_cpt(list_init, list_monomers)
	bound_mono = len(peptides_mono[0])

	print "create clusters count"
	peptides_clust = add_cpt_clusters(peptides_mono, list_clusters)
	bound_clust = len(peptides_clust[0])

	print "create links count"
	peptides_link = add_cpt_link(peptides_clust,5)
	bound_links = len(peptides_link[0])

	print "Data ready to be analyse" 
	
	print bound_init, bound_mono, bound_clust, bound_links

	################################################################
	#####################	LEARNING METHOD  #######################
	################################################################
	
	print "Choose what you want to do :" 
	print "> search c cl mc : "
	print "applied learning method on a base containing just cluster digits, another containine cluster and link associated digits and the last containing monomer and cluster digits"
	print "> compare : "
	print "compare all analyses stocked since the beginning, return a sorted list from the better to the worst digit"
	print "> show cl : "
	print "show the result of the learning method on the cl digits"
	print "> exit : "
	print "quit the program "



	################################################################
	#####################	COMPARE RESULTS  #######################
	################################################################


