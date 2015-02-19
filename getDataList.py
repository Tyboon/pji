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
	liste = [['activity','id','composition']]
	for i in range(1174) : 
		json_data = get_peptide(i)
		json_struct = json.loads(json_data)
		if 'peptides' in json_struct :
			if (len(json_struct['peptides']) >= 1) :
				if (('activity' in json_struct['peptides'][0]['general']) and (len(json_struct['peptides'][0]['general']['activity']) == 1 ) and (json_struct['peptides'][0]['general']['activity'][0] != 'unknown')) :
					if 'id' in json_struct['peptides'][0]['general'] :
						if 'composition' in json_struct['peptides'][0]['structure'] :
							composition = json_struct['peptides'][0]['structure']['composition']
							composition = "'" + composition.replace(', ',';') + "'"
							liste.append([json_struct['peptides'][0]['general']['activity'][0], json_struct['peptides'][0]['general']['id'],composition])
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


if __name__ == "__main__" :
	monomers = get_monomers()
	#print monomers
	print 'get monomers'
	peptides_norine = get_list_peptides()
	print 'get peptides'
	#print peptides_norine
	peptides_count = add_cpt(peptides_norine,monomers)
	print 'get peptides count'
	#print peptides_count
	create_csv(peptides_count,'peptides_final.csv')

