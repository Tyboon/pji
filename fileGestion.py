import csv
from importNorine import *

def create_csv(mylist,filename) :
	'''
	Creates csv from a list
	'''

	csv_file = open(filename, "wb")
	try :
		writer = csv.writer(csv_file)
		for line in mylist :
				#mettre uniquement pour monomers 
				#line  = [line] 
				writer.writerow((line))
	finally :
		csv_file.close()


def read_csv(filename) :
	'''
	Creates list from a csv
	'''
	l = []
	with open(filename, 'rb') as csvfile:
		reader = csv.reader(csvfile, delimiter=',')
		for row in reader :
			l.append(row)
	return l


def read_cluster(myfile) :
	'''
	Permits to read the cluster file
	'''

	with open(myfile,'r') as f:
		liste = []
   		for line in f:
			line = line.lstrip()
			#on filtre les lignes d'infos
			if line : 
				if line[0]=='#' :
					line = line.strip()
					l = []
					l.append(line[1:len(line)])
				else : 
					#line = line.rstrip()
					tab = line.split(';')
					for t in tab :
						l.append(t.rstrip())
					liste.append(l)
	#print liste
	return liste

def load_peptides (peptidesFile) :
	'''
		load the base bdd or Norine by default
	'''
	if peptidesFile == "NORINE" :
		list_init = get_list_peptides() #act, id, compo, lien
	else :
		try :
			list_init = read_csv(peptidesFile) # ajout 1 activite, surfactant
		except IOError :
			print "fichier %s inexistant" % (peptidesFile)
			sys.exit(2)
	return list_init
	
def load_monomers (monomersFile) :
	'''
		load monomers from monomersFile, or from Norine if it's not precised
	'''
	if monomersFile == "NORINE" :
		list_monomers = get_monomers()
	else :
		try :
			list_monomers = read_csv(monomersFile)
		except IOError :
			print "file %s doesn't exist" % (monomersFile)
			sys.exit(2)
	return list_monomers

def load_clusters (clustersFile) :
	'''
		load clusters from clustersFile or data/mono_cluster.csv if it's not precised
	'''
	if clustersFile == "NORINE" :
		list_clusters = read_cluster('data/mono_cluster.csv')
	else :
		try :
			list_monomers = read_cluster(clustersFile)
		except IOError :
			print "file %s doesn't exist" % (clustersFile)
			sys.exit(2)
	return list_clusters


