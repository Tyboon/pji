import urllib2
import csv
import json

'''
	Doc :
	http://pymotw.com/2/json/
	http://www.chicoree.fr/w/Fichiers_CSV_en_Python
'''

'''
	Permit to get all monomers in Json file
'''
def get_monomers() :
	csv_name = "monomeres.csv"
	csv_file = open(csv_name, "wb")
	url = 'http://bioinfo.lifl.fr/norine/rest/monomers/flat/json'
	response = urllib2.urlopen(url).read()
	try :
		writer = csv.writer(csv_file)
		writer.writerow(('num','code'))
		json_struct = json.loads(response)
		num = 0
		for i in json_struct :
			if 'code' in i :
				writer.writerow((`num`,i['code']))
				num += 1
	finally :
		csv_file.close()

'''
	Permits to get a peptide description in Json file
'''
def get_peptide(i) :
	url = 'http://bioinfo.lifl.fr/norine/rest/id/json/NOR'+`i`
	response = urllib2.urlopen(url).read()
	return response

'''
	Permits to get all the peptides description in csv
'''
def get_all_peptides() : 
	csv_name = "peptide.csv"
	csv_file = open(csv_name, "wb")
	try :
		writer = csv.writer(csv_file)
		writer.writerow(('activity','id','composition'))
		for i in range(1,1174) : 
			json_data = get_peptide(i)
			json_struct = json.loads(json_data)
			if 'peptides' in json_struct :
				if (len(json_struct['peptides']) >= 1) :
					if 'activity' in json_struct['peptides'][0]['general'] :
						if 'id' in json_struct['peptides'][0]['general'] :
							if 'composition' in json_struct['peptides'][0]['structure'] :
								composition = json_struct['peptides'][0]['structure']['composition']
								composition = composition.replace(',',';')
								writer.writerow((json_struct['peptides'][0]['general']['activity'][0], json_struct['peptides'][0]['general']['id'],composition))	
	finally :
		csv_file.close()

'''
	Premits to create a list from a csv
'''
def get_list(file) :
	with open(file) as f :
		list_f = []
		for line in csv.reader(f,delimiter=',') :
			list_f.append(line)
	return list_f

'''
	ajoute a la liste les compteurs et les valeurs pour chaque monomeres
'''
def add_cpt(pep,monomere) :
	len_mono = len(monomere)
	len_pep = len(pep)
	#ajout de l'entete
	for m in range(1,len_mono):
		pep[0].append(monomere[m][1])
	
	#ajout des donnees
	for p in range(1,len_pep):
		for m in range(1,len_mono):
			pep[p].append(nb_occ(monomere[m][1],pep[p][2]))
	
	return pep

'''
	Counts the number of occurancies of a monomer in a peptide
'''
def nb_occ(monom, pep) :
	occ = 0
	list_p = pep.split('; ')
	for m in list_p:
		if m == monom :
			occ += 1
	return occ

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
	#print get_peptide(2)
	#get_all_peptides()
	#get_monomers()
	p = get_list('peptide.csv')
	l = get_list('monomeres.csv')
	p = add_cpt(p,l)
	create_csv(p,"peptides_weka.csv")
