import urllib2
import csv
import json

'''
	Permits to get monomers'list
'''
def get_monomers() :
	url = 'http://bioinfo.lifl.fr/norine/rest/monomers/flat/json'
	response = urllib2.urlopen(url).read()
	json_struct = json.loads(response)
	list_monomers = []
	for i in json_struct :
		if 'code' in i :
			list_monomers.append(i['code'])
	return list_monomers

'''
	Permits to get a peptide description in Json file
'''
def get_peptide(i) :
	url = 'http://bioinfo.lifl.fr/norine/rest/id/json/NOR'+`i`
	response = urllib2.urlopen(url).read()
	return response

'''
	Permits to get peptides'list without unknown activity
'''
def get_list_peptides() :
	# Header
	liste = [['activity','id','composition','link']]
	# For all peptides in ddb
	for i in range(400,403) :  #1174 peptides
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
						if (((len(activity) == 1) and (activity[0] != 'unknown')) or ((len(activity) == 2) and (((activity[0]=='surfactant') or (activity[1]=='surfactant')) and ('unknown' not in activity )))) :
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

'''
	Counts the number of occurancies of a monomer in a peptide
'''
def nb_occ(monom, pep) :
	occ = 0
	list_p = pep.split(';')
	occ = list_p.count(monom)
	return occ

'''
	Add to the peptides list the monomers counter
'''
def add_cpt(peptides,monomers) :
	#ajout de l'entete
	for m in monomers:
		peptides[0].append(m)
	
	#ajout des donnees
	for p in peptides :
		if p != peptides[0]:
			for m in monomers:
				p.append(nb_occ(m,p[2]))
	
	return peptides


'''
	Creates csv from a list
'''
def create_csv(mylist,filename) :
	csv_file = open(filename, "wb")
	try :
		writer = csv.writer(csv_file)
		for line in mylist :
				writer.writerow((line))
	finally :
		csv_file.close()


'''
	Permits to read the cluster file
'''
def read_cluster(myfile) :
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
	print liste
	return liste

if __name__ == "__main__" :
	#monomers = get_monomers()
	#print monomers
	#print 'get monomers'
	#peptides_norine = get_list_peptides()
	print 'get peptides'
	#create_csv(peptides_norine,'peptides_tmp.csv')
	#print peptides_norine
	#peptides_count = add_cpt(peptides_norine,monomers)
	print 'get peptides count'
	#print peptides_count
	#create_csv(peptides_count,'peptides_tmp.csv')
	clusters =  read_cluster('data/mono_cluster.csv')
