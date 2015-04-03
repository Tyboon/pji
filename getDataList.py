import urllib2
import csv
import json


def get_monomers() :
	'''
	Permits to get monomers list
	'''

	url = 'http://bioinfo.lifl.fr/norine/rest/monomers/flat/json'
	response = urllib2.urlopen(url).read()
	json_struct = json.loads(response)
	list_monomers = []
	for i in json_struct :
		if 'code' in i :
			list_monomers.append(i['code'])
	return list_monomers


def get_peptide(i) :
	'''
	Permits to get a peptide description in Json file
	'''

	url = 'http://bioinfo.lifl.fr/norine/rest/id/json/NOR'+`i`
	response = urllib2.urlopen(url).read()
	return response

def get_list_peptides() :
	'''
	Permits to get peptides'list without unknown activity
	'''

	# Header
	liste = [['activity','id','composition','link']]
	# For all peptides in ddb
	for i in range(1174) :  #1174 peptides
		print i
		json_data = get_peptide(i)
		json_struct = json.loads(json_data)
		if 'peptides' in json_struct :
			# If there is peptide description continue ... 
			if (len(json_struct['peptides']) >= 1) :
				# If there is activity description continue ...
				if ('activity' in json_struct['peptides'][0]['general']) :
						#Test if there is only 1 activity, or 2 with 'surfactant', and different of 'unknown'
						activity = json_struct['peptides'][0]['general']['activity']
						if (((len(activity) == 1) and (activity[0] != 'unknown') and (activity[0] != 'surfactant')) or ((len(activity) == 2) and (((activity[0]=='surfactant') or (activity[1]=='surfactant')) and ('unknown' not in activity )))) :
							# If there is 'surfactant' remove it from the activity list
							if 'surfactant' in activity :
								activity.remove('surfactant')
								print len(activity)
							# If there is id continue ...
							if 'id' in json_struct['peptides'][0]['general'] :
								# If there is composition description continue ...
								if 'composition' in json_struct['peptides'][0]['structure'] :
									# If ther is link description continue ...
									if 'graph' in json_struct['peptides'][0]['structure'] :
										composition = json_struct['peptides'][0]['structure']['composition']
										composition = "'" + composition.replace(', ',';') + "'"
										lien = json_struct['peptides'][0]['structure']['graph']
										lien = lien.replace(', ',';')
										# Put activity, id, composition and link at the list
										liste.append([activity[0], json_struct['peptides'][0]['general']['id'], composition, lien])
	return liste

def nb_occ(monom, pep) :
	'''
	Counts the number of occurancies of a monomer in a peptide
	'''

	occ = 0
	list_p = pep.split(';')
	occ = list_p.count(monom)
	return occ

def add_cpt(peptides,monomers) :
	'''
	Add to the peptides list the monomers counter
	'''

	#ajout de l'entete
	for m in monomers:
		peptides[0].append(m)
	
	#ajout des donnees
	for p in peptides :
		if p != peptides[0] :
			for m in monomers:
				p.append(nb_occ(m,p[2]))
	
	return peptides


def add_cpt_clusters(peptides, clusters) :
	'''
	Add to the peptides list the cluster counter
	'''
	len_m = len(peptides[0])
	#ajout de l'entete
	for c in clusters :
		peptides[0].append(c[0])

	#ajout des donnees
	for p in peptides :
		if p != peptides[0] :
			for c in clusters :
				p.append(nb_occ_clust(c,p, peptides[0], len_m))
	return peptides


def nb_occ_clust(cluster, pep, header, len_m) :
	'''
	Counts number of occurancies of cluster 
	'''
	cpt = 0
	for i in range(4,len_m) :
		if header[i] in cluster :
			cpt += pep[i]
	return cpt


def select_activity(peptides_clust, N):
	'''
	Select only peptides whose activity counter over N 
	'''

	activities = list(set([row[0] for row in peptides_clust]))
	peptides_act =list([row[0] for row in peptides_clust]) 
	count_act = []
	for a in activities :
		count_act.append((a,peptides_act.count(a)))
	list_count = []
	for c in count_act :
		if c[1] >= 20 :
			list_count.append(c[0])
	print list_count
	
	list_ceil = []
	for p in peptides_clust :
		if p[0] in list_count:
			list_ceil.append(p)
	return list_ceil
	

def create_csv(mylist,filename) :
	'''
	Creates csv from a list
	'''

	csv_file = open(filename, "wb")
	try :
		writer = csv.writer(csv_file)
		for line in mylist :
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

if __name__ == "__main__" :
	#monomers = get_monomers()
	#print monomers
	#print 'get monomers'
	#peptides_norine = get_list_peptides()
	#print 'get peptides'
	#create_csv(peptides_norine,'peptides_tmp.csv')
	#print peptides_norine
	#peptides_count = add_cpt(peptides_norine,monomers)
	#print 'get peptides count'
	#print peptides_count
	#create_csv(peptides_count,'peptides_tmp.csv')
	#clusters =  read_cluster('data/mono_cluster.csv')
	#peptides_clust = add_cpt_clusters(peptides_count, clusters)
	#create_csv(peptides_clust,'peptides_clust.csv')
	print 'get petides clust'
	####################
	peptides_clust = read_csv('peptides_clust.csv')
	print 'get peptides'
	#print peptides_clust
	peptides_ceil = select_activity(peptides_clust, 20)
	create_csv(peptides_ceil, 'peptides_clust_ceil.csv')

