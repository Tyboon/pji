from dataTreatment import *
from fileGestion import *
from learningMethods import * 

from sys import argv
import getopt

import weka.core.jvm as jvm

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
	##################### ANALYSE ARGUMENTS #######################
	peptidesFile, monomersFile, clustersFile, default, selectActivity = start(argv[1:])

	print peptidesFile, monomersFile, clustersFile, default, selectActivity

	##################### LOADING PEPTIDES #########################
	print "Hi, let's start with %s base" % (peptidesFile)

	list_init = load_peptides(peptidesFile,default, selectActivity)  # charge soit norine soit le csv bdd, option par defaut et seuil activite
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

	fileG = "file/peptides_all.csv"

	create_csv(peptides_link, fileG)

	print "Data ready to be analyse" 
	
	print bound_init, bound_mono, bound_clust, bound_links

	################################################################
	#####################	LEARNING METHOD  #######################
	################################################################
	print "Choose what you want to do :" 
	usage()
	rep = raw_input('> ')
	dic = dict()

	jvm.start()
	while ( rep != 'quit' ) :
		words = rep.split(' ')
		
		if ( words[0] == 'learn' ) :
			print 'learn'
			for w in words[1:] : # if several learning todo
				bound = bounding(w, bound_init, bound_mono, bound_clust) # info useless
				l = learning(fileG, bound) 
				dic[w] = l # map [ key = digit, value = learning result]
		
		elif (words[0] == 'compare') :
			print 'compare'

		elif (words[0] == 'show') :
			print 'show'
			for k, v in dic.items() :
				print ("The search {} give us : {}".format(k,v))

		elif (words[0] == 'stock'):
			if len(words) < 2 :
				print 'usage : stock outputFile'
			else :
				stock_csv(words[1], dic)
				print "%s created" % (words[1])

		elif (words[0] == 'help') :
			usage()
		else :
			print "error try again" 
		rep = raw_input('> ')
	print "program ending"
	jvm.stop()
	exit()
	
