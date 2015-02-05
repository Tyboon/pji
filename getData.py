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

if __name__ == "__main__" :
	#print get_peptide(2)
	get_all_peptides()
	#get_monomers()
