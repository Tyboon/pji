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


def loader(peptidesFile, monomersFile, clustersFile, default, selectActivity) :
	
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
	return list_init, list_monomers, list_clusters, bound_init


def create_full_list(list_init, list_mono, list_clusters) :
	print "create monomers count"
	peptides_mono = add_cpt(list_init, list_monomers)
	bound_mono = len(peptides_mono[0])

	print "create clusters count"
	peptides_clust = add_cpt_clusters(peptides_mono, list_clusters)
	bound_clust = len(peptides_clust[0])

	print "create links count"
	peptides_link = add_cpt_link(peptides_clust,5)
	bound_links = len(peptides_link[0])
	
	return peptides_link, bound_mono, bound_clust, bound_links

def launch_report(peptides_link, bi, bm, bc, bl) :
	# Prelevement des donnees X pour data et Y pour targets
	Y = np.array([x[0] for x in peptides_link])
	Y = Y[1:] # delete header
	X = peptides_link[1:] # delete header
	Y, d = numerize(Y)
	
	XM = np.array([x[bi+1:bm] for x in X], dtype=float)
	X_MC = np.array([x[bi+1:bc] for x in X], dtype=float)
	X_ML = np.array([x[bi+1:bm]+x[bc+1:] for x in X], dtype=float)
	X = np.array([x[bi+1:] for x in X], dtype=float)
	
	print('SCORE FOR MONOMERS')
	reportBis(XM,Y,d)
	print('SCORE FOR MONOMERS-CLUSTERS')
	reportBis(X_MC, Y, d)
	print('SCORE FOR MONOMERS-LINKS')
	reportBis(X_ML, Y, d)
	print('SCORE FOR ALL')
	reportBis(X,Y,d)


if  __name__ == "__main__" :
	
	##################### ANALYSE ARGUMENTS #######################
	peptidesFile, monomersFile, clustersFile, default, selectActivity = start(argv[1:])

	print peptidesFile, monomersFile, clustersFile, default, selectActivity
	
	################################################################
		
	###################### LOADING #################################

	list_init, list_monomers, list_clusters, bound_init = loader(peptidesFile, monomersFile, clustersFile, default, selectActivity)

	################################################################
	
	######  GENERATE FULL LIST PEPTIDES (MONO, LINK, CLUST)	#######
	
	peptides_link, bound_mono, bound_clust, bound_link = create_full_list(list_init, list_monomers, list_clusters)
	
	################################################################
	
	##################### GENERATE CSV #############################
	
	fileG = "../file/peptides_all.csv"

	create_csv(peptides_link, fileG)

	print "Data ready to be analyse" 
	
	################################################################
	
	##################### SCORING ##################################
	
	#bound_init, bound_mono, bound_clust, bound_link = 4, 531, 536, 541
	# Chargement du csv sous forme de liste	
	#peptides_link = read_csv('../file/peptides_all.csv')	
	
	#print peptides_link[0][3]
	#print peptides_link[0][531]
	#print peptides_link[0][536]
	#print peptides_link[0][541]

	launch_report(peptides_link, bound_init, bound_mono, bound_clust, bound_link)
